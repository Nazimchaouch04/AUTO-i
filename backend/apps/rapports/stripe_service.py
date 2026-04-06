import stripe
import logging
from django.conf import settings
from django.utils import timezone
from .models import RapportPDF, HistoriqueGeneration

logger = logging.getLogger(__name__)

# Configuration Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    """Service pour la gestion des paiements Stripe"""
    
    @staticmethod
    def creer_payment_intent(rapport_id):
        """Crée un Payment Intent pour un rapport"""
        try:
            rapport = RapportPDF.objects.get(id=rapport_id)
            
            # Crée le Payment Intent
            intent = stripe.PaymentIntent.create(
                amount=int(rapport.prix * 100),  # Convertit en centimes
                currency='eur',
                metadata={
                    'rapport_id': str(rapport.id),
                    'user_id': str(rapport.user.id),
                    'type_rapport': rapport.type_rapport,
                },
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            
            # Sauvegarde l'ID du Payment Intent
            rapport.stripe_payment_intent_id = intent.id
            rapport.save()
            
            logger.info(f"Payment Intent créé: {intent.id} pour rapport {rapport.id}")
            
            return {
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
            }
            
        except RapportPDF.DoesNotExist:
            logger.error(f"Rapport {rapport_id} non trouvé")
            raise ValueError("Rapport non trouvé")
        except stripe.error.StripeError as e:
            logger.error(f"Erreur Stripe création Payment Intent: {e}")
            raise ValueError(f"Erreur paiement: {str(e)}")
        except Exception as e:
            logger.error(f"Erreur création Payment Intent: {e}")
            raise
    
    @staticmethod
    def confirmer_paiement(payment_intent_id):
        """Confirme et traite un paiement réussi"""
        try:
            # Récupère le Payment Intent
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status != 'succeeded':
                logger.warning(f"Payment Intent {payment_intent_id} pas encore réussi: {intent.status}")
                return False
            
            # Trouve le rapport correspondant
            rapport = RapportPDF.objects.get(
                stripe_payment_intent_id=payment_intent_id
            )
            
            # Met à jour le statut
            rapport.statut_paiement = 'paye'
            rapport.save()
            
            # Enregistre l'historique
            HistoriqueGeneration.objects.create(
                rapport=rapport,
                action='paiement',
                statut='succes',
                message=f'Paiement confirmé: {intent.amount / 100}€'
            )
            
            logger.info(f"Paiement confirmé pour rapport {rapport.id}")
            
            # Déclenche la génération du PDF
            from .services import RapportPDFService
            try:
                rapport_service = RapportPDFService()
                rapport_service.generer_pdf(rapport)
            except Exception as e:
                logger.error(f"Erreur génération PDF après paiement: {e}")
                # Le paiement est réussi mais la génération a échoué
                rapport.statut_paiement = 'erreur'
                rapport.save()
                raise
            
            return True
            
        except RapportPDF.DoesNotExist:
            logger.error(f"Aucun rapport trouvé pour Payment Intent {payment_intent_id}")
            return False
        except stripe.error.StripeError as e:
            logger.error(f"Erreur Stripe confirmation paiement: {e}")
            return False
        except Exception as e:
            logger.error(f"Erreur confirmation paiement: {e}")
            return False
    
    @staticmethod
    def creer_session_checkout(rapport_id, success_url, cancel_url):
        """Crée une session Stripe Checkout"""
        try:
            rapport = RapportPDF.objects.get(id=rapport_id)
            
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': f'Rapport {rapport.get_type_rapport_display()}',
                            'description': rapport.titre,
                        },
                        'unit_amount': int(rapport.prix * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'rapport_id': str(rapport.id),
                    'user_id': str(rapport.user.id),
                },
                customer_email=rapport.user.email,
            )
            
            logger.info(f"Session Checkout créée: {session.id} pour rapport {rapport.id}")
            
            return session.url
            
        except RapportPDF.DoesNotExist:
            logger.error(f"Rapport {rapport_id} non trouvé")
            raise ValueError("Rapport non trouvé")
        except stripe.error.StripeError as e:
            logger.error(f"Erreur Stripe création session: {e}")
            raise ValueError(f"Erreur paiement: {str(e)}")
        except Exception as e:
            logger.error(f"Erreur création session Checkout: {e}")
            raise
    
    @staticmethod
    def get_paiement_info(payment_intent_id):
        """Récupère les informations d'un paiement"""
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            return {
                'id': intent.id,
                'status': intent.status,
                'amount': intent.amount / 100,
                'currency': intent.currency,
                'created': timezone.fromtimestamp(intent.created),
                'metadata': intent.metadata,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Erreur Stripe récupération paiement: {e}")
            return None
        except Exception as e:
            logger.error(f"Erreur récupération paiement: {e}")
            return None
    
    @staticmethod
    def creer_refund(payment_intent_id, montant=None):
        """Crée un remboursement"""
        try:
            refund_params = {
                'payment_intent': payment_intent_id,
            }
            
            if montant:
                refund_params['amount'] = int(montant * 100)
            
            refund = stripe.Refund.create(**refund_params)
            
            logger.info(f"Remboursement créé: {refund.id} pour Payment Intent {payment_intent_id}")
            
            return {
                'id': refund.id,
                'amount': refund.amount / 100,
                'status': refund.status,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Erreur Stripe remboursement: {e}")
            raise ValueError(f"Erreur remboursement: {str(e)}")
        except Exception as e:
            logger.error(f"Erreur remboursement: {e}")
            raise
    
    @staticmethod
    def verifier_webhook(payload, sig_header):
        """Vérifie et traite un webhook Stripe"""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            
            logger.info(f"Webhook Stripe reçu: {event.type}")
            
            # Traite les événements
            if event.type == 'payment_intent.succeeded':
                payment_intent = event.data.object
                StripeService.confirmer_paiement(payment_intent.id)
            
            elif event.type == 'payment_intent.payment_failed':
                payment_intent = event.data.object
                StripeService._traiter_echec_paiement(payment_intent)
            
            elif event.type == 'checkout.session.completed':
                session = event.data.object
                StripeService._traiter_session_completee(session)
            
            return True
            
        except stripe.error.SignatureVerificationError:
            logger.error("Signature webhook invalide")
            return False
        except Exception as e:
            logger.error(f"Erreur traitement webhook: {e}")
            return False
    
    @staticmethod
    def _traiter_echec_paiement(payment_intent):
        """Traite un échec de paiement"""
        try:
            rapport = RapportPDF.objects.get(
                stripe_payment_intent_id=payment_intent.id
            )
            
            rapport.statut_paiement = 'erreur'
            rapport.save()
            
            HistoriqueGeneration.objects.create(
                rapport=rapport,
                action='paiement',
                statut='erreur',
                message=f'Échec paiement: {payment_intent.last_payment_error.message if payment_intent.last_payment_error else "Inconnu"}'
            )
            
            logger.info(f"Échec paiement enregistré pour rapport {rapport.id}")
            
        except RapportPDF.DoesNotExist:
            logger.error(f"Rapport non trouvé pour échec paiement {payment_intent.id}")
    
    @staticmethod
    def _traiter_session_completee(session):
        """Traite une session Checkout complétée"""
        try:
            rapport_id = session.metadata.get('rapport_id')
            if rapport_id:
                rapport = RapportPDF.objects.get(id=rapport_id)
                rapport.statut_paiement = 'paye'
                rapport.save()
                
                # Déclenche la génération
                from .services import RapportPDFService
                rapport_service = RapportPDFService()
                rapport_service.generer_pdf(rapport)
                
                logger.info(f"Session Checkout complétée pour rapport {rapport_id}")
            
        except Exception as e:
            logger.error(f"Erreur traitement session Checkout: {e}")

# Webhook handler pour Django
def stripe_webhook_view(request):
    """Vue Django pour traiter les webhooks Stripe"""
    from django.http import JsonResponse
    from django.views.decorators.csrf import csrf_exempt
    import json
    
    @csrf_exempt
    def _webhook_view(request):
        if request.method != 'POST':
            return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
        
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        if StripeService.verifier_webhook(payload, sig_header):
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'error': 'Webhook invalide'}, status=400)
    
    return _webhook_view(request)
