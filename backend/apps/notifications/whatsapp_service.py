import logging
from decouple import config
from .models import CanalNotification, NotificationHistory

logger = logging.getLogger(__name__)

TWILIO_SID = config('TWILIO_ACCOUNT_SID', default='')
TWILIO_TOKEN = config('TWILIO_AUTH_TOKEN', default='')
TWILIO_FROM = config('TWILIO_WHATSAPP_FROM', default='whatsapp:+14155238886')

def envoyer_whatsapp(to_number, message):
    """Envoie un message WhatsApp via Twilio."""
    if not TWILIO_SID:
        logger.warning("Twilio non configuré - Simulation du message")
        print(f"WhatsApp vers {to_number}: {message[:100]}...")
        return True
    
    try:
        from twilio.rest import Client
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        
        msg = client.messages.create(
            body=message,
            from_=TWILIO_FROM,
            to=f'whatsapp:{to_number}'
        )
        
        logger.info(f"Message WhatsApp envoyé à {to_number} - SID: {msg.sid}")
        return msg.sid is not None
        
    except Exception as e:
        logger.error(f"Erreur WhatsApp: {e}")
        return False

def formater_alerte_whatsapp(annonce, alerte):
    """Formate un message d'alerte WhatsApp."""
    ecart = ""
    if annonce.ecart_prix and annonce.ecart_prix < 0:
        ecart = f"🔥 {abs(annonce.ecart_prix):.0f}% sous le marché\n"
    
    # Formatage du prix
    prix_str = f"{annonce.prix:,.0f} €".replace(',', ' ')
    
    # Formatage du kilométrage
    km_str = f"{annonce.kilometrage:,} km".replace(',', ' ')
    
    # Estimation si disponible
    estimation_str = ""
    if annonce.prix_estime:
        estime_str = f"{annonce.prix_estime:,.0f} €".replace(',', ' ')
        estimation_str = f"\n📊 Estimation marché : {estime_str}"
    
    # URL de l'annonce
    annonce_url = f"https://autointel.vercel.app/annonces/{annonce.id}"
    
    message = f"""🚗 *Bonne affaire détectée !*

{ecart}*{annonce.vehicule.marque} {annonce.vehicule.modele} {annonce.annee}*
💰 {prix_str} · {km_str}
📍 {annonce.ville or 'N/A'} · {annonce.pays}{estimation_str}

Voir : {annonce_url}
_(Alerte : {alerte.nom})_"""
    
    return message

def envoyer_message_test_whatsapp(to_number):
    """Envoie un message de test pour vérifier la connexion WhatsApp."""
    message = """🤖 *Test AutoIntel*

✅ Votre numéro WhatsApp est bien configuré !

Vous recevrez maintenant les alertes de bonnes affaires directement sur WhatsApp.

_Configuration terminée avec succès !_"""
    
    return envoyer_whatsapp(to_number, message)

def valider_numero_whatsapp(numero):
    """Valide le format d'un numéro WhatsApp."""
    if not numero.startswith('+'):
        return False, "Le numéro doit commencer par + (ex: +213)"
    
    numero_clean = numero.replace('+', '')
    if not numero_clean.isdigit():
        return False, "Le numéro ne doit contenir que des chiffres"
    
    if len(numero_clean) < 10 or len(numero_clean) > 15:
        return False, "Le numéro doit contenir entre 10 et 15 chiffres"
    
    return True, "Numéro valide"

def get_twilio_status():
    """Vérifie le statut de la configuration Twilio."""
    if not TWILIO_SID:
        return {
            'configured': False,
            'message': 'TWILIO_ACCOUNT_SID non configuré'
        }
    
    if not TWILIO_TOKEN:
        return {
            'configured': False,
            'message': 'TWILIO_AUTH_TOKEN non configuré'
        }
    
    return {
        'configured': True,
        'message': 'Twilio configuré',
        'from_number': TWILIO_FROM
    }
