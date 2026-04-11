from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Avg, F, Sum
from django.utils import timezone
from django.http import HttpResponse
import csv
import json
from datetime import datetime, timedelta

from .models import Annonce, Favori, RechercheSauvegardee
from .models_advanced import (
    HistoriqueRecherche, Signalement, VisiteAnnonce, ContactVendeur,
    EvaluationVendeur, NotificationAnnonce, ComparaisonAnnonce,
    AlerteRecherche, StatistiqueAnnonce
)
from .serializers import (
    AnnonceSerializer, FavoriSerializer, RechercheSauvegardeeSerializer,
    SignalementSerializer, EvaluationVendeurSerializer, ComparaisonAnnonceSerializer,
    AlerteRechercheSerializer
)


class AnnonceViewSet(viewsets.ModelViewSet):
    """ViewSet avancé pour les annonces avec fonctionnalités améliorées"""
    serializer_class = AnnonceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Annonce.objects.filter(est_active=True)
        
        # Filtrage avancé
        marque = self.request.query_params.get('marque')
        modele = self.request.query_params.get('modele')
        prix_min = self.request.query_params.get('prix_min')
        prix_max = self.request.query_params.get('prix_max')
        km_min = self.request.query_params.get('km_min')
        km_max = self.request.query_params.get('km_max')
        annee_min = self.request.query_params.get('annee_min')
        annee_max = self.request.query_params.get('annee_max')
        carburant = self.request.query_params.get('carburant')
        boite = self.request.query_params.get('boite')
        pays = self.request.query_params.get('pays')
        ville = self.request.query_params.get('ville')
        recherche = self.request.query_params.get('recherche')
        tri = self.request.query_params.get('tri', '-date_publication')
        bonnes_affaires = self.request.query_params.get('bonnes_affaires')
        
        if marque:
            queryset = queryset.filter(vehicule__marque__icontains=marque)
        if modele:
            queryset = queryset.filter(vehicule__modele__icontains=modele)
        if prix_min:
            queryset = queryset.filter(prix__gte=prix_min)
        if prix_max:
            queryset = queryset.filter(prix__lte=prix_max)
        if km_min:
            queryset = queryset.filter(kilometrage__gte=km_min)
        if km_max:
            queryset = queryset.filter(kilometrage__lte=km_max)
        if annee_min:
            queryset = queryset.filter(annee__gte=annee_min)
        if annee_max:
            queryset = queryset.filter(annee__lte=annee_max)
        if carburant:
            queryset = queryset.filter(carburant=carburant)
        if boite:
            queryset = queryset.filter(boite=boite)
        if pays:
            queryset = queryset.filter(pays=pays)
        if ville:
            queryset = queryset.filter(ville__icontains=ville)
        if recherche:
            queryset = queryset.filter(
                Q(vehicule__marque__icontains=recherche) |
                Q(vehicule__modele__icontains=recherche) |
                Q(description__icontains=recherche) |
                Q(ville__icontains=recherche)
            )
        if bonnes_affaires == 'true':
            queryset = queryset.filter(est_bonne_affaire=True)
        
        # Tri avancé
        if tri == 'prix_croissant':
            queryset = queryset.order_by('prix')
        elif tri == 'prix_decroissant':
            queryset = queryset.order_by('-prix')
        elif tri == 'km_croissant':
            queryset = queryset.order_by('kilometrage')
        elif tri == 'km_decroissant':
            queryset = queryset.order_by('-kilometrage')
        elif tri == 'annee_croissant':
            queryset = queryset.order_by('annee')
        elif tri == 'annee_decroissant':
            queryset = queryset.order_by('-annee')
        elif tri == 'score_affaire':
            queryset = queryset.order_by('-score_affaire')
        else:
            queryset = queryset.order_by('-date_publication')
        
        return queryset.select_related('vehicule').prefetch_related('favoris_selectionnes')
    
    def retrieve(self, request, *args, **kwargs):
        """Récupération détaillée d'une annonce avec statistiques"""
        instance = self.get_object()
        
        # Enregistrement de la visite
        if request.user.is_authenticated:
            VisiteAnnonce.objects.create(
                annonce=instance,
                utilisateur=request.user,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                provient_de=request.META.get('HTTP_REFERER', '')
            )
        
        # Mise à jour des statistiques
        instance.vues = F('vues') + 1
        instance.save(update_fields=['vues'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def ajouter_favori(self, request, pk=None):
        """Ajouter une annonce aux favoris"""
        annonce = self.get_object()
        favori, created = Favori.objects.get_or_create(
            user=request.user,
            annonce=annonce
        )
        
        if created:
            # Mise à jour du compteur de favoris
            annonce.sauvegardes = F('sauvegardes') + 1
            annonce.save(update_fields=['sauvegardes'])
            
            # Notification
            NotificationAnnonce.objects.create(
                utilisateur=request.user,
                type_notification='favori_ajoute',
                titre='Favori ajouté',
                message=f'{annonce.vehicule.marque} {annonce.vehicule.modele} a été ajouté à vos favoris',
                annonce=annonce
            )
            
            return Response({'message': 'Ajouté aux favoris'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Déjà dans les favoris'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def retirer_favori(self, request, pk=None):
        """Retirer une annonce des favoris"""
        annonce = self.get_object()
        try:
            favori = Favori.objects.get(user=request.user, annonce=annonce)
            favori.delete()
            
            # Mise à jour du compteur de favoris
            annonce.sauvegardes = F('sauvegardes') - 1
            annonce.save(update_fields=['sauvegardes'])
            
            return Response({'message': 'Retiré des favoris'})
        except Favori.DoesNotExist:
            return Response({'error': 'Pas dans les favoris'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def contacter_vendeur(self, request, pk=None):
        """Contacter le vendeur d'une annonce"""
        annonce = self.get_object()
        message = request.data.get('message', '')
        telephone = request.data.get('telephone', '')
        
        if not message:
            return Response({'error': 'Message requis'}, status=status.HTTP_400_BAD_REQUEST)
        
        contact = ContactVendeur.objects.create(
            annonce=annonce,
            acheteur_potentiel=request.user,
            message=message,
            telephone_contact=telephone,
            email_contact=request.user.email
        )
        
        # Mise à jour du compteur de contacts
        annonce.contacts = F('contacts') + 1
        annonce.save(update_fields=['contacts'])
        
        # Notification pour le vendeur
        NotificationAnnonce.objects.create(
            utilisateur=annonce.vendeur,
            type_notification='nouveau_contact',
            titre='Nouveau contact pour votre annonce',
            message=f'{request.user.username} est intéressé par votre annonce {annonce.vehicule.marque} {annonce.vehicule.modele}',
            annonce=annonce
        )
        
        return Response({'message': 'Message envoyé au vendeur'}, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def signaler(self, request, pk=None):
        """Signaler une annonce"""
        annonce = self.get_object()
        raison = request.data.get('raison')
        description = request.data.get('description', '')
        
        if not raison:
            return Response({'error': 'Raison requise'}, status=status.HTTP_400_BAD_REQUEST)
        
        signalement, created = Signalement.objects.get_or_create(
            annonce=annonce,
            utilisateur=request.user,
            defaults={
                'raison': raison,
                'description': description
            }
        )
        
        if created:
            return Response({'message': 'Annonce signalée'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Annonce déjà signalée'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def evaluer_vendeur(self, request, pk=None):
        """Évaluer le vendeur après contact"""
        annonce = self.get_object()
        note = request.data.get('note')
        commentaire = request.data.get('commentaire', '')
        aspects = request.data.get('aspects', {})
        
        if not note or note < 1 or note > 5:
            return Response({'error': 'Note invalide (1-5)'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Vérifier si l'utilisateur a contacté le vendeur
        if not ContactVendeur.objects.filter(annonce=annonce, acheteur_potentiel=request.user).exists():
            return Response({'error': 'Vous devez contacter le vendeur avant de l\'évaluer'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        evaluation, created = EvaluationVendeur.objects.get_or_create(
            vendeur=annonce.vendeur,
            evaluateur=request.user,
            annonce=annonce,
            defaults={
                'note': note,
                'commentaire': commentaire,
                'aspects': aspects
            }
        )
        
        if created:
            return Response({'message': 'Évaluation enregistrée'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Évaluation déjà enregistrée'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mes_favoris(self, request):
        """Liste des favoris de l'utilisateur"""
        favoris = Favori.objects.filter(user=request.user).select_related('annonce__vehicule')
        annonces = [f.annonce for f in favoris]
        serializer = AnnonceSerializer(annonces, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mes_contacts(self, request):
        """Historique des contacts de l'utilisateur"""
        contacts = ContactVendeur.objects.filter(
            acheteur_potentiel=request.user
        ).select_related('annonce__vehicule').order_by('-date_contact')
        
        data = []
        for contact in contacts:
            data.append({
                'id': contact.id,
                'annonce': {
                    'id': contact.annonce.id,
                    'titre': f"{contact.annonce.vehicule.marque} {contact.annonce.vehicule.modele}",
                    'prix': contact.annonce.prix,
                    'image': contact.annonce.images[0] if contact.annonce.images else None
                },
                'message': contact.message,
                'date_contact': contact.date_contact,
                'est_repondu': contact.est_repondu
            })
        
        return Response(data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mes_evaluations(self, request):
        """Évaluations données par l'utilisateur"""
        evaluations = EvaluationVendeur.objects.filter(
            evaluateur=request.user
        ).select_related('annonce__vehicule', 'vendeur').order_by('-date_evaluation')
        
        data = []
        for eval in evaluations:
            data.append({
                'id': eval.id,
                'annonce': {
                    'id': eval.annonce.id,
                    'titre': f"{eval.annonce.vehicule.marque} {eval.annonce.vehicule.modele}",
                },
                'vendeur': eval.vendeur.username,
                'note': eval.note,
                'commentaire': eval.commentaire,
                'aspects': eval.aspects,
                'date_evaluation': eval.date_evaluation
            })
        
        return Response(data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def statistiques_personnelles(self, request):
        """Statistiques personnelles de l'utilisateur"""
        user = request.user
        
        # Statistiques générales
        stats = {
            'annonces_vues': VisiteAnnonce.objects.filter(utilisateur=user).count(),
            'favoris_ajoutes': Favori.objects.filter(user=user).count(),
            'contacts_envoyes': ContactVendeur.objects.filter(acheteur_potentiel=user).count(),
            'evaluations_donnees': EvaluationVendeur.objects.filter(evaluateur=user).count(),
            'signalements_envoyes': Signalement.objects.filter(utilisateur=user).count(),
            'recherches_effectuees': HistoriqueRecherche.objects.filter(user=user).count(),
        }
        
        # Marques préférées
        marques_preferees = (
            Favori.objects.filter(user=user)
            .values('annonce__vehicule__marque')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        )
        
        # Prix moyen consulté
        prix_moyen = (
            VisiteAnnonce.objects.filter(utilisateur=user)
            .aggregate(avg_prix=Avg('annonce__prix'))['avg_prix'] or 0
        )
        
        # Activité récente
        activite_recente = []
        
        # Derniers favoris
        derniers_favoris = (
            Favori.objects.filter(user=user)
            .select_related('annonce__vehicule')
            .order_by('-created_at')[:3]
        )
        for fav in derniers_favoris:
            activite_recente.append({
                'type': 'favori',
                'titre': f"{fav.annonce.vehicule.marque} {fav.annonce.vehicule.modele}",
                'date': fav.created_at,
                'annonce_id': fav.annonce.id
            })
        
        # Derniers contacts
        derniers_contacts = (
            ContactVendeur.objects.filter(acheteur_potentiel=user)
            .select_related('annonce__vehicule')
            .order_by('-date_contact')[:3]
        )
        for contact in derniers_contacts:
            activite_recente.append({
                'type': 'contact',
                'titre': f"{contact.annonce.vehicule.marque} {contact.annonce.vehicule.modele}",
                'date': contact.date_contact,
                'annonce_id': contact.annonce.id
            })
        
        # Trier par date
        activite_recente.sort(key=lambda x: x['date'], reverse=True)
        
        return Response({
            'stats_generales': stats,
            'marques_preferees': list(marques_preferees),
            'prix_moyen_consulte': float(prix_moyen),
            'activite_recente': activite_recente[:10]
        })


class RechercheAvanceeViewSet(viewsets.GenericViewSet):
    """ViewSet pour la recherche avancée et les filtres intelligents"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def suggestions(self, request):
        """Suggestions de recherche intelligentes"""
        terme = request.query_params.get('terme', '')
        
        if len(terme) < 2:
            return Response({'suggestions': []})
        
        # Suggestions de marques
        marques = Annonce.objects.filter(
            vehicule__marque__icontains=terme
        ).values_list('vehicule__marque', flat=True).distinct()[:5]
        
        # Suggestions de modèles
        modeles = Annonce.objects.filter(
            vehicule__modele__icontains=terme
        ).values_list('vehicule__modele', flat=True).distinct()[:5]
        
        # Suggestions de villes
        villes = Annonce.objects.filter(
            ville__icontains=terme
        ).values_list('ville', flat=True).distinct()[:5]
        
        return Response({
            'marques': list(marques),
            'modeles': list(modeles),
            'villes': list(villes)
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def recherches_similaires(self, request):
        """Recherches similaires basées sur l'historique"""
        user = request.user
        
        # Récupérer les dernières recherches
        dernieres_recherches = (
            HistoriqueRecherche.objects.filter(user=user)
            .order_by('-date_recherche')[:10]
        )
        
        suggestions = []
        for recherche in dernieres_recherches:
            # Trouver des annonces similaires
            annonces_similaires = Annonce.objects.filter(
                Q(vehicule__marque__icontains=recherche.terme) |
                Q(vehicule__modele__icontains=recherche.terme)
            ).filter(est_active=True)[:3]
            
            if annonces_similaires.exists():
                suggestions.append({
                    'terme': recherche.terme,
                    'nombre_resultats': annonces_similaires.count(),
                    'derniere_recherche': recherche.date_recherche,
                    'exemples': [
                        {
                            'id': annonce.id,
                            'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele}",
                            'prix': annonce.prix,
                            'image': annonce.images[0] if annonce.images else None
                        }
                        for annonce in annonces_similaires
                    ]
                })
        
        return Response(suggestions)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def sauvegarder_recherche(self, request):
        """Sauvegarder une recherche avec des filtres"""
        terme = request.data.get('terme', '')
        filtres = request.data.get('filtres', {})
        nom = request.data.get('nom', f'Recherche {timezone.now().strftime("%d/%m/%Y")}')
        
        # Compter les résultats
        queryset = Annonce.objects.filter(est_active=True)
        
        # Appliquer les filtres
        for key, value in filtres.items():
            if key == 'marque' and value:
                queryset = queryset.filter(vehicule__marque__icontains=value)
            elif key == 'prix_min' and value:
                queryset = queryset.filter(prix__gte=value)
            elif key == 'prix_max' and value:
                queryset = queryset.filter(prix__lte=value)
            elif key == 'km_max' and value:
                queryset = queryset.filter(kilometrage__lte=value)
        
        nombre_resultats = queryset.count()
        
        # Sauvegarder la recherche
        recherche = RechercheSauvegardee.objects.create(
            user=request.user,
            nom=nom,
            query_params={'terme': terme, 'filtres': filtres},
            result_count=nombre_resultats
        )
        
        # Enregistrer dans l'historique
        HistoriqueRecherche.objects.create(
            user=request.user,
            terme=terme,
            filtres=filtres,
            nombre_resultats=nombre_resultats
        )
        
        serializer = RechercheSauvegardeeSerializer(recherche)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExportViewSet(viewsets.GenericViewSet):
    """ViewSet pour l'export de données"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def export_favoris(self, request):
        """Exporter les favoris en CSV"""
        favoris = Favori.objects.filter(user=request.user).select_related('annonce__vehicule')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="favoris_autointel.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Marque', 'Modèle', 'Année', 'Kilométrage', 'Prix', 
            'Ville', 'Pays', 'Date ajout', 'Lien'
        ])
        
        for favori in favoris:
            annonce = favori.annonce
            writer.writerow([
                annonce.vehicule.marque,
                annonce.vehicule.modele,
                annonce.annee,
                annonce.kilometrage,
                annonce.prix,
                annonce.ville,
                annonce.pays,
                favori.created_at.strftime('%d/%m/%Y'),
                f"http://localhost:5173/annonce/{annonce.id}"
            ])
        
        return response
    
    @action(detail=False, methods=['get'])
    def export_statistiques(self, request):
        """Exporter les statistiques personnelles"""
        user = request.user
        
        stats = {
            'utilisateur': user.username,
            'date_export': timezone.now().strftime('%d/%m/%Y %H:%M'),
            'statistiques': {
                'annonces_vues': VisiteAnnonce.objects.filter(utilisateur=user).count(),
                'favoris_ajoutes': Favori.objects.filter(user=user).count(),
                'contacts_envoyes': ContactVendeur.objects.filter(acheteur_potentiel=user).count(),
                'evaluations_donnees': EvaluationVendeur.objects.filter(evaluateur=user).count(),
            },
            'marques_preferees': list(
                Favori.objects.filter(user=user)
                .values('annonce__vehicule__marque')
                .annotate(count=Count('id'))
                .order_by('-count')[:10]
            ),
            'recherches_recentes': list(
                HistoriqueRecherche.objects.filter(user=user)
                .values('terme', 'nombre_resultats', 'date_recherche')
                .order_by('-date_recherche')[:20]
            )
        }
        
        response = HttpResponse(
            json.dumps(stats, indent=2, default=str), 
            content_type='application/json'
        )
        response['Content-Disposition'] = 'attachment; filename="statistiques_autointel.json"'
        
        return response
