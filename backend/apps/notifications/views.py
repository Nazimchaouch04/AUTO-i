from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import CanalNotification, NotificationHistory
from .telegram_service import (
    envoyer_message_test_telegram, 
    verifier_chat_id, 
    get_bot_info
)
from .whatsapp_service import (
    envoyer_message_test_whatsapp, 
    valider_numero_whatsapp,
    get_twilio_status
)
import logging

logger = logging.getLogger(__name__)

class CanauxNotificationView(APIView):
    """Gestion des canaux de notification de l'utilisateur."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Liste les canaux de notification de l'utilisateur."""
        canaux = CanalNotification.objects.filter(user=request.user)
        
        data = []
        for canal in canaux:
            canal_data = {
                'id': canal.id,
                'canal': canal.canal,
                'valeur': canal.valeur,
                'is_verified': canal.is_verified,
                'is_active': canal.is_active,
                'created_at': canal.created_at,
                'display_valeur': self._mask_sensitive_info(canal)
            }
            data.append(canal_data)
        
        return Response(data)

    def post(self, request):
        """Ajoute un nouveau canal de notification."""
        canal_type = request.data.get('canal')
        valeur = request.data.get('valeur', '').strip()
        
        if not canal_type or not valeur:
            return Response({
                'error': 'Le type de canal et la valeur sont requis'
            }, status=400)
        
        if canal_type not in ['email', 'telegram', 'whatsapp']:
            return Response({
                'error': 'Type de canal non valide'
            }, status=400)
        
        try:
            # Validation spécifique selon le type
            if canal_type == 'telegram':
                if not verifier_chat_id(valeur):
                    return Response({
                        'error': 'Chat ID Telegram invalide'
                    }, status=400)
            
            elif canal_type == 'whatsapp':
                is_valid, message = valider_numero_whatsapp(valeur)
                if not is_valid:
                    return Response({'error': message}, status=400)
            
            # Crée ou met à jour le canal
            canal, created = CanalNotification.objects.update_or_create(
                user=request.user,
                canal=canal_type,
                defaults={'valeur': valeur, 'is_verified': False}
            )
            
            return Response({
                'id': canal.id,
                'canal': canal.canal,
                'valeur': canal.valeur,
                'is_verified': canal.is_verified,
                'created': created
            }, status=201 if created else 200)
            
        except Exception as e:
            logger.error(f"Erreur ajout canal {canal_type}: {e}")
            return Response({
                'error': 'Erreur lors de l\'ajout du canal'
            }, status=500)

    def _mask_sensitive_info(self, canal):
        """Masque les informations sensibles pour l'affichage."""
        if canal.canal == 'email':
            email = canal.valeur
            if '@' in email:
                local, domain = email.split('@', 1)
                masked_local = local[:2] + '*' * (len(local) - 2)
                return f"{masked_local}@{domain}"
            return email
        
        elif canal.canal == 'whatsapp':
            numero = canal.valeur
            if len(numero) > 6:
                return numero[:3] + '*' * (len(numero) - 6) + numero[-3:]
            return numero
        
        elif canal.canal == 'telegram':
            return canal.valeur  # Chat ID n'est pas vraiment sensible
        
        return canal.valeur

class VerifierCanalView(APIView):
    """Vérifie et teste un canal de notification."""
    permission_classes = [IsAuthenticated]

    def post(self, request, canal_id):
        canal = get_object_or_404(CanalNotification, id=canal_id, user=request.user)
        
        try:
            success = False
            message = ""
            
            if canal.canal == 'telegram':
                success = envoyer_message_test_telegram(canal.valeur)
                message = "Message de test envoyé avec succès" if success else "Échec de l'envoi"
                if success:
                    canal.is_verified = True
                    canal.save()
            
            elif canal.canal == 'whatsapp':
                success = envoyer_message_test_whatsapp(canal.valeur)
                message = "Message de test envoyé avec succès" if success else "Échec de l'envoi"
                if success:
                    canal.is_verified = True
                    canal.save()
            
            elif canal.canal == 'email':
                # Pour l'email, on considère comme vérifié par défaut
                canal.is_verified = True
                canal.save()
                success = True
                message = "Email marqué comme vérifié"
            
            return Response({
                'success': success,
                'message': message,
                'is_verified': canal.is_verified
            })
            
        except Exception as e:
            logger.error(f"Erreur vérification canal {canal_id}: {e}")
            return Response({
                'error': 'Erreur lors de la vérification'
            }, status=500)

class SupprimerCanalView(APIView):
    """Supprime un canal de notification."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, canal_id):
        canal = get_object_or_404(CanalNotification, id=canal_id, user=request.user)
        canal.delete()
        return Response({'message': 'Canal supprimé avec succès'})

class ActiverCanalView(APIView):
    """Active/désactive un canal de notification."""
    permission_classes = [IsAuthenticated]

    def patch(self, request, canal_id):
        canal = get_object_or_404(CanalNotification, id=canal_id, user=request.user)
        canal.is_active = request.data.get('is_active', not canal.is_active)
        canal.save()
        
        return Response({
            'id': canal.id,
            'is_active': canal.is_active,
            'message': f'Canal {"activé" if canal.is_active else "désactivé"}'
        })

class NotificationStatusView(APIView):
    """Statut des services de notification."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retourne le statut des différents services."""
        telegram_status = {
            'configured': bool(get_bot_info()),
            'message': 'Configuré' if get_bot_info() else 'Non configuré',
            'bot_info': get_bot_info()
        }
        
        whatsapp_status = get_twilio_status()
        
        return Response({
            'telegram': telegram_status,
            'whatsapp': whatsapp_status
        })

class HistoriqueNotificationsView(APIView):
    """Historique des notifications envoyées."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retourne l'historique des notifications de l'utilisateur."""
        historique = NotificationHistory.objects.filter(
            canal__user=request.user
        ).select_related('canal', 'annonce', 'alerte').order_by('-created_at')[:50]
        
        data = []
        for notif in historique:
            item = {
                'id': notif.id,
                'canal': notif.canal.canal,
                'contenu': notif.contenu[:100] + '...' if len(notif.contenu) > 100 else notif.contenu,
                'statut': notif.statut,
                'created_at': notif.created_at,
                'sent_at': notif.sent_at
            }
            
            if notif.annonce:
                item['annonce'] = {
                    'id': notif.annonce.id,
                    'titre': f"{notif.annonce.vehicule.marque} {notif.annonce.vehicule.modele}",
                    'prix': notif.annonce.prix
                }
            
            if notif.alerte:
                item['alerte'] = {
                    'id': notif.alerte.id,
                    'nom': notif.alerte.nom
                }
            
            data.append(item)
        
        return Response(data)
