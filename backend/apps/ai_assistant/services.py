import anthropic
from django.conf import settings
from decouple import config
from apps.annonces.models import Annonce, Vehicule
from django.db.models import Avg, Count, Min, Max, Q
import logging

logger = logging.getLogger(__name__)

# Initialisation du client Anthropic
ANTHROPIC_API_KEY = config('ANTHROPIC_API_KEY', default='')
if ANTHROPIC_API_KEY:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
else:
    client = None
    logger.warning("ANTHROPIC_API_KEY non configurée - L'assistant IA ne fonctionnera pas")

def get_contexte_marche():
    """Récupère les données réelles du marché pour contextualiser l'IA."""
    try:
        stats = Annonce.objects.filter(est_active=True).aggregate(
            total=Count('id'),
            prix_moyen=Avg('prix'),
            bonnes_affaires=Count('id', filter=Q(est_bonne_affaire=True))
        )
        
        top_marques = list(
            Annonce.objects.filter(est_active=True)
            .values('vehicule__marque')
            .annotate(nb=Count('id'), prix_moyen=Avg('prix'))
            .order_by('-nb')[:8]
        )
        
        # S'assurer que les valeurs ne sont pas None
        stats['total'] = stats['total'] or 0
        stats['prix_moyen'] = stats['prix_moyen'] or 0
        stats['bonnes_affaires'] = stats['bonnes_affaires'] or 0
        
        return stats, top_marques
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du contexte marché: {e}")
        # Retourner des valeurs par défaut
        return {'total': 0, 'prix_moyen': 0, 'bonnes_affaires': 0}, []

def construire_system_prompt():
    """Construit le prompt système pour Claude avec les données du marché."""
    stats, top_marques = get_contexte_marche()
    
    marques_str = ', '.join([
        f"{m['vehicule__marque']} (moy. {int(m['prix_moyen'] or 0):,}€)"
        for m in top_marques if m['vehicule__marque']
    ])
    
    return f"""Tu es AutoIntel Assistant, un expert en analyse du marché automobile
au Maghreb (Algérie, Tunisie, Maroc) et en France.

DONNÉES ACTUELLES DU MARCHÉ :
- Total annonces actives : {stats['total']:,}
- Prix moyen du marché : {int(stats['prix_moyen']):,}€
- Bonnes affaires détectées : {stats['bonnes_affaires']:,}
- Top marques : {marques_str if marques_str else 'Aucune donnée disponible'}

TON RÔLE :
- Analyser si une voiture est bien ou mal prix selon le marché
- Donner des conseils d'achat/vente personnalisés
- Expliquer les tendances du marché automobile local
- Aider l'utilisateur à comprendre les estimations ML
- Répondre en français, de façon concise et professionnelle

RÈGLES :
- Toujours baser tes réponses sur les données réelles du marché
- Mentionner les prix en Euros ET en DA (1€ ≈ 145 DA) si pertinent
- Si tu manques d'info sur un véhicule précis, dis-le clairement
- Maximum 3-4 paragraphes par réponse
- Proposer d'estimer le prix via la page Estimation si pertinent
- Sois amical et professionnel dans tes réponses"""

def envoyer_message(conversation, user_message, abonnement=None):
    """Envoie un message à Claude et retourne la réponse."""
    
    if not client:
        return {
            'content': "L'assistant IA n'est pas disponible actuellement. "
                      "Veuillez contacter l'administrateur pour configurer l'API Claude.",
            'limited': True
        }
    
    try:
        # Vérifie les limites selon le plan
        from .models import UsageIA
        from django.utils import timezone
        usage, _ = UsageIA.objects.get_or_create(
            user=conversation.user,
            date=timezone.now().date()
        )
        
        limite = 5 if not abonnement or abonnement.plan.nom == 'free' else 999
        if usage.messages_utilises >= limite:
            return {
                'content': f"Tu as atteint ta limite de {limite} messages par jour. "
                          "Passe au plan Pro pour des messages illimités ! 🚀",
                'limited': True
            }

        # Récupère l'historique de la conversation (max 10 derniers messages)
        historique = list(conversation.messages.order_by('-created_at')[:10])
        historique.reverse()

        messages_api = []
        for msg in historique:
            messages_api.append({'role': msg.role, 'content': msg.content})
        messages_api.append({'role': 'user', 'content': user_message})

        # Appel Claude API
        response = client.messages.create(
            model='claude-3-sonnet-20240229',  # Utiliser un modèle disponible
            max_tokens=1024,
            system=construire_system_prompt(),
            messages=messages_api
        )

        assistant_reply = response.content[0].text

        # Sauvegarde les messages
        from .models import Message
        Message.objects.create(
            conversation=conversation, role='user', content=user_message)
        Message.objects.create(
            conversation=conversation, role='assistant', content=assistant_reply)

        # Met à jour le compteur d'usage
        usage.messages_utilises += 1
        usage.save()

        # Génère un titre automatique si c'est le premier message
        if conversation.messages.count() == 2:
            conversation.titre = user_message[:60] + ('...' if len(user_message) > 60 else '')
            conversation.save()

        return {'content': assistant_reply, 'limited': False}
        
    except anthropic.APIError as e:
        logger.error(f"Erreur API Claude: {e}")
        return {
            'content': "Une erreur technique est survenue avec l'assistant IA. "
                      "Veuillez réessayer dans quelques instants.",
            'limited': False
        }
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du message: {e}")
        return {
            'content': "Une erreur inattendue est survenue. "
                      "Veuillez réessayer ou contacter le support.",
            'limited': False
        }
