from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404, FileResponse
from django.utils import timezone
from .models import RapportPDF, TemplateRapport, HistoriqueGeneration
from .services import RapportPDFService
from .stripe_service import StripeService
import logging

logger = logging.getLogger(__name__)

class RapportsListView(APIView):
    """Liste des rapports de l'utilisateur"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retourne la liste des rapports de l'utilisateur"""
        rapports = RapportPDF.objects.filter(user=request.user).select_related(
            'annonce_principale', 'alerte_source'
        ).prefetch_related('annonces_comparees')
        
        data = []
        for rapport in rapports:
            item = {
                'id': rapport.id,
                'type_rapport': rapport.type_rapport,
                'type_display': rapport.get_type_rapport_display(),
                'titre': rapport.titre,
                'prix': rapport.prix,
                'statut_paiement': rapport.statut_paiement,
                'statut_display': rapport.get_statut_paiement_display(),
                'created_at': rapport.created_at,
                'genere_at': rapport.genere_at,
                'expire_at': rapport.expire_at,
                'est_valide': rapport.est_valide,
                'peut_etre_telecharge': rapport.peut_etre_telecharge,
            }
            
            # Informations sur l'annonce principale
            if rapport.annonce_principale:
                item['annonce'] = {
                    'id': rapport.annonce_principale.id,
                    'titre': f"{rapport.annonce_principale.vehicule.marque} {rapport.annonce_principale.vehicule.modele} {rapport.annonce_principale.annee}",
                    'prix': rapport.annonce_principale.prix,
                }
            
            # Nombre d'annonces comparées
            if rapport.type_rapport == 'comparatif':
                item['nb_annonces_comparees'] = rapport.annonces_comparees.count()
            
            data.append(item)
        
        return Response(data)

class CreerRapportView(APIView):
    """Création d'un nouveau rapport"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Crée un nouveau rapport PDF"""
        try:
            type_rapport = request.data.get('type_rapport')
            titre = request.data.get('titre')
            
            if not type_rapport or not titre:
                return Response({
                    'error': 'Le type de rapport et le titre sont requis'
                }, status=400)
            
            # Validation du type
            types_valides = [choice[0] for choice in RapportPDF.TYPE_RAPPORT_CHOICES]
            if type_rapport not in types_valides:
                return Response({
                    'error': 'Type de rapport invalide'
                }, status=400)
            
            # Crée le rapport
            rapport_service = RapportPDFService()
            rapport = rapport_service.creer_rapport(
                user=request.user,
                type_rapport=type_rapport,
                titre=titre,
                annonce_principale_id=request.data.get('annonce_principale_id'),
                alerte_source_id=request.data.get('alerte_source_id'),
            )
            
            # Ajoute les annonces comparées si nécessaire
            if type_rapport == 'comparatif':
                annonces_ids = request.data.get('annonces_comparees', [])
                rapport.annonces_comparees.set(annonces_ids)
            
            return Response({
                'id': rapport.id,
                'type_rapport': rapport.type_rapport,
                'titre': rapport.titre,
                'prix': rapport.prix,
                'statut_paiement': rapport.statut_paiement,
                'created_at': rapport.created_at,
            }, status=201)
            
        except Exception as e:
            logger.error(f"Erreur création rapport: {e}")
            return Response({
                'error': 'Erreur lors de la création du rapport'
            }, status=500)

class PayerRapportView(APIView):
    """Paiement d'un rapport avec Stripe"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, rapport_id):
        """Crée un Payment Intent pour le rapport"""
        try:
            rapport = get_object_or_404(RapportPDF, id=rapport_id, user=request.user)
            
            if rapport.statut_paiement != 'en_attente':
                return Response({
                    'error': 'Ce rapport a déjà été payé ou n\'est pas payable'
                }, status=400)
            
            # Crée le Payment Intent
            payment_data = StripeService.creer_payment_intent(rapport_id)
            
            return Response({
                'client_secret': payment_data['client_secret'],
                'payment_intent_id': payment_data['payment_intent_id'],
                'prix': rapport.prix,
            })
            
        except ValueError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            logger.error(f"Erreur paiement rapport {rapport_id}: {e}")
            return Response({
                'error': 'Erreur lors de la création du paiement'
            }, status=500)

class CheckoutRapportView(APIView):
    """Création d'une session Stripe Checkout"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, rapport_id):
        """Crée une session Checkout pour le rapport"""
        try:
            rapport = get_object_or_404(RapportPDF, id=rapport_id, user=request.user)
            
            if rapport.statut_paiement != 'en_attente':
                return Response({
                    'error': 'Ce rapport a déjà été payé ou n\'est pas payable'
                }, status=400)
            
            # URLs de retour
            success_url = request.data.get('success_url', f"{request.build_absolute_uri('/')}rapports/success/")
            cancel_url = request.data.get('cancel_url', f"{request.build_absolute_uri('/')}rapports/cancel/")
            
            # Crée la session Checkout
            checkout_url = StripeService.creer_session_checkout(
                rapport_id, success_url, cancel_url
            )
            
            return Response({
                'checkout_url': checkout_url,
                'prix': rapport.prix,
            })
            
        except ValueError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            logger.error(f"Erreur checkout rapport {rapport_id}: {e}")
            return Response({
                'error': 'Erreur lors de la création du paiement'
            }, status=500)

class TelechargerRapportView(APIView):
    """Téléchargement d'un rapport PDF"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, rapport_id):
        """Retourne le fichier PDF du rapport"""
        try:
            rapport = get_object_or_404(RapportPDF, id=rapport_id, user=request.user)
            
            if not rapport.peut_etre_telecharge:
                return Response({
                    'error': 'Ce rapport n\'est pas disponible au téléchargement'
                }, status=403)
            
            # Enregistre le téléchargement
            HistoriqueGeneration.objects.create(
                rapport=rapport,
                action='telechargement',
                statut='succes',
                message='Téléchargement du PDF'
            )
            
            # Retourne le fichier
            response = FileResponse(
                rapport.fichier_pdf.open('rb'),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="rapport_{rapport.id}.pdf"'
            response['X-Content-Type-Options'] = 'nosniff'
            
            return response
            
        except Http404:
            return Response({'error': 'Rapport non trouvé'}, status=404)
        except Exception as e:
            logger.error(f"Erreur téléchargement rapport {rapport_id}: {e}")
            return Response({
                'error': 'Erreur lors du téléchargement'
            }, status=500)

class DetailRapportView(APIView):
    """Détails d'un rapport"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, rapport_id):
        """Retourne les détails complets d'un rapport"""
        try:
            rapport = get_object_or_404(RapportPDF, id=rapport_id, user=request.user)
            
            data = {
                'id': rapport.id,
                'type_rapport': rapport.type_rapport,
                'type_display': rapport.get_type_rapport_display(),
                'titre': rapport.titre,
                'prix': rapport.prix,
                'statut_paiement': rapport.statut_paiement,
                'statut_display': rapport.get_statut_paiement_display(),
                'created_at': rapport.created_at,
                'genere_at': rapport.genere_at,
                'expire_at': rapport.expire_at,
                'est_valide': rapport.est_valide,
                'peut_etre_telecharge': rapport.peut_etre_telecharge,
                'contenu_json': rapport.contenu_json if rapport.statut_paiement == 'termine' else None,
            }
            
            # Informations sur l'annonce principale
            if rapport.annonce_principale:
                data['annonce_principale'] = {
                    'id': rapport.annonce_principale.id,
                    'titre': f"{rapport.annonce_principale.vehicule.marque} {rapport.annonce_principale.vehicule.modele} {rapport.annonce_principale.annee}",
                    'prix': rapport.annonce_principale.prix,
                    'kilometrage': rapport.annonce_principale.kilometrage,
                    'ville': rapport.annonce_principale.ville,
                }
            
            # Annonces comparées
            if rapport.type_rapport == 'comparatif':
                data['annonces_comparees'] = [
                    {
                        'id': a.id,
                        'titre': f"{a.vehicule.marque} {a.vehicule.modele} {a.annee}",
                        'prix': a.prix,
                        'kilometrage': a.kilometrage,
                    } for a in rapport.annonces_comparees.all()
                ]
            
            # Historique
            historique = HistoriqueGeneration.objects.filter(rapport=rapport).order_by('-created_at')[:10]
            data['historique'] = [
                {
                    'action': h.action,
                    'statut': h.statut,
                    'message': h.message,
                    'created_at': h.created_at,
                    'temps_execution': h.temps_execution,
                } for h in historique
            ]
            
            return Response(data)
            
        except Http404:
            return Response({'error': 'Rapport non trouvé'}, status=404)
        except Exception as e:
            logger.error(f"Erreur détails rapport {rapport_id}: {e}")
            return Response({
                'error': 'Erreur lors de la récupération des détails'
            }, status=500)

class SupprimerRapportView(APIView):
    """Suppression d'un rapport"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, rapport_id):
        """Supprime un rapport"""
        try:
            rapport = get_object_or_404(RapportPDF, id=rapport_id, user=request.user)
            
            # Supprime le fichier PDF s'il existe
            if rapport.fichier_pdf:
                rapport.fichier_pdf.delete()
            
            # Supprime le rapport
            titre = rapport.titre
            rapport.delete()
            
            return Response({
                'message': f'Rapport "{titre}" supprimé avec succès'
            })
            
        except Http404:
            return Response({'error': 'Rapport non trouvé'}, status=404)
        except Exception as e:
            logger.error(f"Erreur suppression rapport {rapport_id}: {e}")
            return Response({
                'error': 'Erreur lors de la suppression'
            }, status=500)

class TypesRapportView(APIView):
    """Liste des types de rapports disponibles"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retourne les types de rapports avec descriptions"""
        types = [
            {
                'type': 'complet',
                'nom': 'Rapport Complet',
                'description': 'Analyse détaillée d\'une annonce avec comparaison au marché',
                'prix': '9.99€',
                'delai': 'Génération instantanée',
            },
            {
                'type': 'comparatif',
                'nom': 'Analyse Comparative',
                'description': 'Comparaison entre plusieurs annonces similaires',
                'prix': '14.99€',
                'delai': 'Génération instantanée',
            },
            {
                'type': 'historique',
                'nom': 'Historique Prix',
                'description': 'Évolution des prix sur une période donnée',
                'prix': '19.99€',
                'delai': 'Génération instantanée',
            },
            {
                'type': 'estimation',
                'nom': 'Rapport d\'Estimation',
                'description': 'Estimation précise avec facteurs d\'influence',
                'prix': '12.99€',
                'delai': 'Génération instantanée',
            },
        ]
        
        return Response(types)

class StatistiquesRapportsView(APIView):
    """Statistiques sur les rapports de l'utilisateur"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retourne les statistiques des rapports"""
        try:
            rapports = RapportPDF.objects.filter(user=request.user)
            
            stats = {
                'total_rapports': rapports.count(),
                'rapports_payes': rapports.filter(statut_paiement='termine').count(),
                'rapports_en_attente': rapports.filter(statut_paiement='en_attente').count(),
                'total_depense': sum(r.prix for r in rapports.filter(statut_paiement='termine')),
                'rapports_par_type': {},
                'rapports_recent': [],
            }
            
            # Statistiques par type
            for type_choice in RapportPDF.TYPE_RAPPORT_CHOICES:
                type_key = type_choice[0]
                count = rapports.filter(type_rapport=type_key).count()
                if count > 0:
                    stats['rapports_par_type'][type_key] = {
                        'nom': type_choice[1],
                        'count': count,
                    }
            
            # Rapports récents
            recent = rapports.order_by('-created_at')[:5]
            stats['rapports_recent'] = [
                {
                    'id': r.id,
                    'titre': r.titre,
                    'type_display': r.get_type_rapport_display(),
                    'statut_display': r.get_statut_paiement_display(),
                    'created_at': r.created_at,
                } for r in recent
            ]
            
            return Response(stats)
            
        except Exception as e:
            logger.error(f"Erreur statistiques rapports: {e}")
            return Response({
                'error': 'Erreur lors de la récupération des statistiques'
            }, status=500)
