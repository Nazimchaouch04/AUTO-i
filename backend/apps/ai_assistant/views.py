from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, UsageIA
from .services import envoyer_message
import logging

logger = logging.getLogger(__name__)

class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Liste des conversations de l'utilisateur."""
        try:
            convs = Conversation.objects.filter(
                user=request.user).order_by('-updated_at')[:20]
            
            data = []
            for c in convs:
                # Récupère le dernier message
                dernier_msg = c.messages.last()
                dernier_msg_text = ""
                if dernier_msg:
                    dernier_msg_text = dernier_msg.content[:50] + ('...' if len(dernier_msg.content) > 50 else '')
                
                data.append({
                    'id': c.id,
                    'titre': c.titre,
                    'updated_at': c.updated_at,
                    'created_at': c.created_at,
                    'dernier_message': dernier_msg_text,
                    'nb_messages': c.messages.count()
                })
            
            return Response(data)
        except Exception as e:
            logger.error(f"Erreur récupération conversations: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)

    def post(self, request):
        """Crée une nouvelle conversation."""
        try:
            conv = Conversation.objects.create(user=request.user)
            return Response({
                'id': conv.id, 
                'titre': conv.titre,
                'created_at': conv.created_at
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Erreur création conversation: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)


class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conv_id):
        """Récupère les messages d'une conversation."""
        try:
            conv = get_object_or_404(Conversation, id=conv_id, user=request.user)
            messages = conv.messages.order_by('created_at')
            
            data = []
            for m in messages:
                data.append({
                    'id': m.id,
                    'role': m.role, 
                    'content': m.content,
                    'created_at': m.created_at
                })
            
            return Response(data)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation non trouvée'}, status=404)
        except Exception as e:
            logger.error(f"Erreur récupération messages: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)

    def post(self, request, conv_id):
        """Envoie un message dans une conversation."""
        try:
            conv = get_object_or_404(Conversation, id=conv_id, user=request.user)
            user_message = request.data.get('message', '').strip()
            
            if not user_message:
                return Response({'error': 'Message vide'}, status=400)

            # Récupère l'abonnement de l'utilisateur
            abonnement = getattr(request.user, 'abonnement', None)
            result = envoyer_message(conv, user_message, abonnement)
            
            return Response(result)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation non trouvée'}, status=404)
        except Exception as e:
            logger.error(f"Erreur envoi message: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)


class MessageRapideView(APIView):
    """Crée automatiquement une conversation et envoie un message."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            message = request.data.get('message', '').strip()
            if not message:
                return Response({'error': 'Message vide'}, status=400)

            conv = Conversation.objects.create(user=request.user)
            abonnement = getattr(request.user, 'abonnement', None)
            result = envoyer_message(conv, message, abonnement)
            result['conversation_id'] = conv.id
            
            return Response(result)
        except Exception as e:
            logger.error(f"Erreur message rapide: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)


class UsageStatsView(APIView):
    """Statistiques d'utilisation pour l'utilisateur."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            from django.utils import timezone
            from datetime import timedelta
            
            today = timezone.now().date()
            usage_today, _ = UsageIA.objects.get_or_create(
                user=request.user,
                date=today
            )
            
            # Statistiques des 7 derniers jours
            week_ago = today - timedelta(days=7)
            week_usage = UsageIA.objects.filter(
                user=request.user,
                date__gte=week_ago
            ).aggregate(total=UsageIA.objects.filter(
                user=request.user,
                date__gte=week_ago
            ).aggregate(total=models.Sum('messages_utilises'))['total'] or 0)
            
            # Limite selon l'abonnement
            abonnement = getattr(request.user, 'abonnement', None)
            limite = 999 if abonnement and abonnement.plan.nom != 'free' else 5
            
            return Response({
                'messages_aujourdhui': usage_today.messages_utilises,
                'limite_journaliere': limite,
                'messages_restants': max(0, limite - usage_today.messages_utilises),
                'total_semaine': week_usage['total']
            })
        except Exception as e:
            logger.error(f"Erreur stats usage: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)


class SupprimerConversationView(APIView):
    """Supprime une conversation et tous ses messages."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, conv_id):
        try:
            conv = get_object_or_404(Conversation, id=conv_id, user=request.user)
            conv.delete()
            return Response({'message': 'Conversation supprimée'})
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation non trouvée'}, status=404)
        except Exception as e:
            logger.error(f"Erreur suppression conversation: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)
