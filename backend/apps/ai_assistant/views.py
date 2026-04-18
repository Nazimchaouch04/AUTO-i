from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Avg, Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import (
    Conversation, Message, UsageIA, UserProfileAnalysis, 
    VehicleRecommendation, MarketInsight, IntentAnalysis
)
from . import services as ai_services
from .services.simple_nlp_service import SimpleNLPService, SimpleUserProfileAnalyzer
from .services.predictive_analytics import PredictiveAnalyticsService
import logging

logger = logging.getLogger(__name__)


PREDICTIVE_FILTER_KEYS = [
    'vehicule_id', 'marque', 'marques', 'modele', 'categorie', 'carburant',
    'pays', 'annee_min', 'annee_max', 'prix_min', 'prix_max'
]


def _extract_predictive_filters(payload):
    filters = payload.get('filters', {})
    if not isinstance(filters, dict):
        filters = {}

    extracted = dict(filters)
    for key in PREDICTIVE_FILTER_KEYS:
        value = payload.get(key)
        if value not in (None, '', [], {}):
            extracted[key] = value
    return extracted


def _to_int_or_default(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


class AIAssistantRootView(APIView):
    """
    Vue racine pour l'AI Assistant - liste les endpoints disponibles
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retourne la liste des endpoints de l'AI Assistant disponibles
        """
        base_url = "/api/ai/"
        endpoints = [
            {
                "path": "conversations/",
                "method": "GET",
                "description": "Voir la liste des conversations"
            },
            {
                "path": "conversations/",
                "method": "POST",
                "description": "Créer une nouvelle conversation"
            },
            {
                "path": "conversations/<id>/messages/",
                "method": "GET",
                "description": "Voir les messages d'une conversation"
            },
            {
                "path": "conversations/<id>/messages/",
                "method": "POST",
                "description": "Envoyer un message dans une conversation"
            },
            {
                "path": "message-rapide/",
                "method": "POST",
                "description": "Envoyer un message rapide sans conversation"
            },
            {
                "path": "usage-stats/",
                "method": "GET",
                "description": "Voir les statistiques d'utilisation de l'IA"
            },
            {
                "path": "market-insights/",
                "method": "GET",
                "description": "Voir les tendances predictives du marche"
            },
            {
                "path": "prediction-prix/",
                "method": "POST",
                "description": "Projeter l'evolution des prix d'un segment ou vehicule"
            },
            {
                "path": "analyse-predictive/",
                "method": "GET/POST",
                "description": "Generer un rapport predictif personnalise avec donnees externes"
            }
        ]
        
        return Response({
            "message": "Bienvenue dans l'AI Assistant AutoIntel!",
            "conversations": f"{base_url}conversations/",
            "quick_message": f"{base_url}message-rapide/",
            "usage_stats": f"{base_url}usage-stats/",
            "predictive_analysis": f"{base_url}analyse-predictive/",
            "endpoints": endpoints
        })

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
            result = ai_services.envoyer_message(conv, user_message, abonnement)
            
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
            result = ai_services.envoyer_message(conv, message, abonnement)
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
            ).aggregate(total=Sum('messages_utilises'))
            
            # Limite selon l'abonnement
            abonnement = getattr(request.user, 'abonnement', None)
            limite = 999 if abonnement and abonnement.plan.nom != 'free' else 5
            
            return Response({
                'messages_aujourdhui': usage_today.messages_utilises,
                'limite_journaliere': limite,
                'messages_restants': max(0, limite - usage_today.messages_utilises),
                'total_semaine': week_usage['total'] or 0
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


class AnalyserMessageView(APIView):
    """Analyse un message avec NLP avancé."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            message_text = request.data.get('message', '').strip()
            if not message_text:
                return Response({'error': 'Message vide'}, status=400)

            nlp_service = SimpleNLPService()
            analyse = nlp_service.analyser_message(message_text)

            # Mettre à jour le profil utilisateur
            profile_analyzer = SimpleUserProfileAnalyzer(request.user)
            profil_ia = profile_analyzer.mettre_a_jour_profil_ia(message_text)

            return Response({
                'analyse': analyse,
                'profil_mis_a_jour': True,
                'profil_ia': {
                    'budget_max': profil_ia.budget_max,
                    'budget_min': profil_ia.budget_min,
                    'marques_preferrees': [m.nom for m in profil_ia.marques_preferrees.all()],
                    'types_vehicule': profil_ia.types_vehicule,
                    'preferences_carburant': profil_ia.preferences_carburant,
                    'usage_principal': profil_ia.usage_principal,
                    'scores': {
                        'budget': profil_ia.score_budget,
                        'ecologique': profil_ia.score_ecologique,
                        'praticite': profil_ia.score_praticite
                    }
                }
            })
        except Exception as e:
            logger.error(f"Erreur analyse message: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)


class RecommandationsVehiculesView(APIView):
    """Génère des recommandations de véhicules personnalisées."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Temporairement retourné des données de test
            return Response({
                'recommandations': [
                    {
                        'id': 1,
                        'vehicule': {
                            'marque': 'Renault',
                            'modele': 'Clio',
                            'prix_moyen': 15000,
                            'type_carburant': 'essence',
                            'nombre_places': 5
                        },
                        'scores': {'total': 85, 'prix': 20, 'besoins': 25, 'marche': 20, 'disponibilite': 20},
                        'raisons': ['Excellent rapport qualité-prix', 'Faible consommation'],
                        'points_forts': ['Fiabilité reconnue', 'Coût d\'entretien faible'],
                        'points_faibles': ['Design daté'],
                        'predictions': {'prix_1an': 13500, 'prix_3ans': 11000, 'confiance': 75}
                    }
                ],
                'total': 1,
                'message': 'Mode démo - Recommandations simplifiées'
            })
        except Exception as e:
            logger.error(f"Erreur recommandations: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)

    def post(self, request):
        """Génère des recommandations avec des filtres personnalisés."""
        try:
            return Response({
                'recommandations': [],
                'message': 'Mode démo - Fonctionnalité en développement'
            })
        except Exception as e:
            logger.error(f"Erreur recommandations personnalisées: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)


class ProfilIAView(APIView):
    """Gestion du profil IA de l'utilisateur."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profil, created = UserProfileAnalysis.objects.get_or_create(user=request.user)

            return Response({
                'budget_max': profil.budget_max,
                'budget_min': profil.budget_min,
                'marques_preferrees': [m.nom for m in profil.marques_preferrees.all()],
                'types_vehicule': profil.types_vehicule,
                'preferences_carburant': profil.preferences_carburant,
                'usage_principal': profil.usage_principal,
                'kilometrage_annuel': profil.kilometrage_annuel,
                'places_minimales': profil.places_minimales,
                'porte_minimales': profil.porte_minimales,
                'transmission_preferree': profil.transmission_preferree,
                'scores': {
                    'budget': profil.score_budget,
                    'ecologique': profil.score_ecologique,
                    'praticite': profil.score_praticite
                },
                'created_at': profil.created_at,
                'updated_at': profil.updated_at
            })
        except Exception as e:
            logger.error(f"Erreur récupération profil IA: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)

    def put(self, request):
        """Met à jour le profil IA manuellement."""
        try:
            profil, created = UserProfileAnalysis.objects.get_or_create(user=request.user)

            # Mise à jour des champs
            if 'budget_max' in request.data:
                profil.budget_max = request.data['budget_max']
            if 'budget_min' in request.data:
                profil.budget_min = request.data['budget_min']
            if 'usage_principal' in request.data:
                profil.usage_principal = request.data['usage_principal']
            if 'kilometrage_annuel' in request.data:
                profil.kilometrage_annuel = request.data['kilometrage_annuel']
            if 'places_minimales' in request.data:
                profil.places_minimales = request.data['places_minimales']
            if 'porte_minimales' in request.data:
                profil.porte_minimales = request.data['porte_minimales']
            if 'transmission_preferree' in request.data:
                profil.transmission_preferree = request.data['transmission_preferree']

            # Mise à jour des listes
            if 'marques_preferrees' in request.data:
                profil.marques_preferrees.clear()
                for marque_nom in request.data['marques_preferrees']:
                    from vehicules.models import Marque
                    try:
                        marque = Marque.objects.get(nom__iexact=marque_nom)
                        profil.marques_preferrees.add(marque)
                    except Marque.DoesNotExist:
                        pass

            if 'types_vehicule' in request.data:
                profil.types_vehicule = request.data['types_vehicule']

            if 'preferences_carburant' in request.data:
                profil.preferences_carburant = request.data['preferences_carburant']

            # Recalculer les scores
            profile_analyzer = SimpleUserProfileAnalyzer(request.user)
            profil.score_budget = profile_analyzer._calculer_score_budget(profil)
            profil.score_ecologique = profile_analyzer._calculer_score_ecologique(profil)
            profil.score_praticite = profile_analyzer._calculer_score_praticite(profil)

            profil.save()

            return Response({'message': 'Profil IA mis à jour avec succès'})
        except Exception as e:
            logger.error(f"Erreur mise à jour profil IA: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)


class MarketInsightsView(APIView):
    """Aperçus et tendances du marché."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            filters = _extract_predictive_filters(request.query_params)
            lookback_months = _to_int_or_default(
                request.query_params.get('lookback_months'),
                12,
            )
            service = PredictiveAnalyticsService(request.user)
            report = service.build_predictive_report(
                filters=filters,
                forecast_months=6,
                lookback_months=lookback_months,
            )
            return Response({
                'insights': report['market_insights'],
                'total': len(report['market_insights']),
                'resume_marche': report['price_forecast']['summary'],
                'meilleures_periodes': report['best_periods'],
                'message': 'Analyse predictive generee'
            })
            return Response({
                'insights': [
                    {
                        'id': 1,
                        'titre': 'Tendance des prix: +2.1% ce mois-ci',
                        'description': 'Les prix du marché automobile ont augmenté de 2.1% ce mois-ci. C\'est le moment d\'acheter avant que les prix n\'augmentent davantage.',
                        'type': 'tendance_prix',
                        'niveau_impact': 65,
                        'confiance': 85,
                        'marques_concernees': ['Renault', 'Peugeot'],
                        'categories_vehicules': ['SUV', 'Berline'],
                        'fourchettes_prix': {'min': 10000, 'max': 50000}
                    }
                ],
                'total': 1,
                'message': 'Mode démo - Insights simplifiés'
            })
        except Exception as e:
            logger.error(f"Erreur market insights: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)


class PredictionPrixView(APIView):
    """Prédiction de prix pour un véhicule."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            filters = _extract_predictive_filters(request.data)
            annees = request.data.get('annees', [])
            forecast_months = _to_int_or_default(
                request.data.get('forecast_months'),
                6,
            )
            if annees:
                try:
                    forecast_months = max(
                        forecast_months,
                        max(int(annee) for annee in annees) * 12,
                    )
                except (TypeError, ValueError):
                    forecast_months = max(forecast_months, 6)

            service = PredictiveAnalyticsService(request.user)
            report = service.build_predictive_report(
                filters=filters,
                forecast_months=forecast_months,
                lookback_months=_to_int_or_default(
                    request.data.get('lookback_months'),
                    12,
                ),
                external_context=request.data.get('external_context') or {},
            )

            queryset = service._build_queryset(report['scope']['filters'])
            sample_annonce = queryset.first()

            predictions_payload = {}
            requested_years = annees or [1, 3]
            for annee in requested_years:
                try:
                    months = int(annee) * 12
                except (TypeError, ValueError):
                    continue
                forecast_points = report['price_forecast']['forecast']
                if not forecast_points or months <= 0 or months > len(forecast_points):
                    continue
                point = forecast_points[months - 1]
                predictions_payload[f'{int(annee)}_ans'] = {
                    'prix_estime': point['predicted_price'],
                    'confiance': point['confidence'],
                    'variation_pourcentage': point['change_vs_current_pct'],
                }

            if not predictions_payload:
                for point in report['price_forecast']['forecast'][:3]:
                    predictions_payload[point['period']] = {
                        'prix_estime': point['predicted_price'],
                        'confiance': point['confidence'],
                        'variation_pourcentage': point['change_vs_current_pct'],
                    }

            return Response({
                'vehicule': {
                    'marque': (sample_annonce.marque.nom if sample_annonce else None) or filters.get('marque'),
                    'modele': (sample_annonce.modele if sample_annonce else None) or filters.get('modele'),
                    'prix_actuel': report['price_forecast']['current_average_price']
                },
                'predictions': predictions_payload,
                'forecast': report['price_forecast']['forecast'],
                'historique': report['price_forecast']['historical_series'],
                'meilleures_periodes': report['best_periods'],
                'impact_evenements': report['event_impact'],
                'resume': report['price_forecast']['summary'],
                'message': 'Analyse predictive generee'
            })
            vehicule_id = request.data.get('vehicule_id')
            annees = request.data.get('annees', [1, 3, 5])

            if not vehicule_id:
                return Response({'error': 'vehicule_id requis'}, status=400)

            return Response({
                'vehicule': {
                    'id': vehicule_id,
                    'marque': 'Renault',
                    'modele': 'Clio',
                    'prix_actuel': 15000
                },
                'predictions': {
                    '1_ans': {'prix_estime': 13500, 'confiance': 75, 'variation_pourcentage': -10},
                    '3_ans': {'prix_estime': 11000, 'confiance': 65, 'variation_pourcentage': -27}
                },
                'message': 'Mode démo - Prédictions simplifiées'
            })
        except Exception as e:
            logger.error(f"Erreur prediction prix: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)


class AnalysePredictiveView(APIView):
    """Rapport predictif complet du marche."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self._build_report(request.query_params, request.user)

    def post(self, request):
        return self._build_report(request.data, request.user)

    def _build_report(self, payload, user):
        try:
            service = PredictiveAnalyticsService(user)
            report = service.build_predictive_report(
                filters=_extract_predictive_filters(payload),
                external_context=payload.get('external_context') or {},
                forecast_months=_to_int_or_default(payload.get('forecast_months'), 6),
                lookback_months=_to_int_or_default(payload.get('lookback_months'), 12),
            )
            return Response(report)
        except Exception as e:
            logger.error(f"Erreur analyse predictive: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)


class ConversationIntelligenteView(APIView):
    """Conversation intelligente avec recommandations intégrées."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Message intelligent avec analyse et recommandations automatiques."""
        try:
            conv_id = request.data.get('conversation_id')
            message = request.data.get('message', '').strip()

            if not message:
                return Response({'error': 'Message vide'}, status=400)

            # Créer ou récupérer la conversation
            if conv_id:
                conv = get_object_or_404(Conversation, id=conv_id, user=request.user)
            else:
                conv = Conversation.objects.create(user=request.user)

            # Analyser le message avec NLP simplifié
            nlp_service = SimpleNLPService()
            analyse = nlp_service.analyser_message(message)

            # Mettre à jour le profil utilisateur
            profile_analyzer = SimpleUserProfileAnalyzer(request.user)
            profil_ia = profile_analyzer.mettre_a_jour_profil_ia(message)

            # Créer l'analyse d'intention
            user_msg = Message.objects.create(
                conversation=conv,
                role='user',
                content=message
            )

            IntentAnalysis.objects.create(
                message=user_msg,
                intent_principale=analyse['intent_principale'],
                entites=analyse['entites'],
                sentiment=analyse['sentiment'],
                niveau_urgence=analyse['niveau_urgence'],
                contexte_conversation=analyse['contexte_conversation']
            )

            # Générer la réponse de l'IA simplifiée
            reponse_ia = self._generer_reponse_intelligente(analyse, profil_ia)

            # Créer le message de l'assistant
            assistant_msg = Message.objects.create(
                conversation=conv,
                role='assistant',
                content=reponse_ia['texte']
            )

            # Mettre à jour l'utilisation
            today = timezone.now().date()
            usage, _ = UsageIA.objects.get_or_create(user=request.user, date=today)
            usage.messages_utilises += 1
            usage.save()

            return Response({
                'conversation_id': conv.id,
                'message_id': assistant_msg.id,
                'reponse': reponse_ia,
                'analyse': analyse,
                'recommandations': [],
                'profil_mis_a_jour': True,
                'message': 'Mode démo - Conversation simplifiée'
            })
        except Exception as e:
            logger.error(f"Erreur conversation intelligente: {e}")
            return Response({'error': 'Erreur serveur'}, status=500)

    def _generer_reponse_intelligente(self, analyse: dict, profil: UserProfileAnalysis) -> dict:
        """Génère une réponse intelligente basée sur l'analyse."""
        intent = analyse['intent_principale']
        entites = analyse['entites']
        
        reponses_base = {
            'recherche_vehicule': "Je vais vous aider à trouver le véhicule parfait. D'après vos préférences, ",
            'conseil_achat': "Voici mes conseils pour votre achat automobile. ",
            'estimation_prix': "Laissez-moi analyser les prix du marché pour vous. ",
            'information_marche': "Voici les informations actuelles du marché automobile. ",
            'comparaison': "Je vais vous aider à comparer ces véhicules. ",
            'avis_expert': "Voici mon avis d'expert sur votre question. ",
            'autre': "Je suis là pour vous aider avec l'automobile. "
        }
        
        texte = reponses_base.get(intent, reponses_base['autre'])
        
        # Ajouter des détails spécifiques selon l'intention
        if intent == 'recherche_vehicule':
            if entites.get('budget'):
                texte += f"votre budget de {entites['budget']}EUR "
            if entites.get('marques'):
                marques = ', '.join(entites['marques'][:2])
                texte += f"et vos préférences pour les marques {marques} "
            texte += "me permettent de vous recommander les véhicules les plus adaptés."
            
        elif intent == 'conseil_achat':
            if profil.score_budget > 70:
                texte += "Votre budget est assez flexible, ce qui vous donne plus d'options."
            else:
                texte += "Avec un budget plus serré, je vous conseille de cibler les véhicules avec une bonne décote."
                
        elif intent == 'estimation_prix':
            texte += "J'analyse les tendances actuelles et les données du marché pour vous donner l'estimation la plus précise possible."
        
        return {
            'texte': texte,
            'intent_detecte': intent,
            'confiance': 85,
            'suggestions': self._generer_suggestions(intent, entites)
        }
    
    def _generer_suggestions(self, intent: str, entites: dict) -> list:
        """Génère des suggestions de suivi."""
        suggestions = []
        
        if intent == 'recherche_vehicule':
            if not entites.get('budget'):
                suggestions.append("Quel est votre budget maximum ?")
            if not entites.get('marques'):
                suggestions.append("Avez-vous des préférences de marques ?")
            suggestions.append("Quel sera l'usage principal du véhicule ?")
            
        elif intent == 'conseil_achat':
            suggestions.append("Voulez-vous voir les recommandations actuelles ?")
            suggestions.append("Préférez-vous acheter neuf ou occasion ?")
            
        return suggestions[:3]
