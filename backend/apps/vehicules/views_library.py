from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q, Avg, Count, F
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import csv
import json

from .models_library import (
    Marque, Modele, Motorisation, Finition, Equipement,
    AvisExpert, ProblemeCourant, DonneeMarche
)
from .serializers_library import (
    MarqueSerializer, ModeleSerializer, MotorisationSerializer,
    FinitionSerializer, EquipementSerializer, AvisExpertSerializer,
    ProblemeCourantSerializer, DonneeMarcheSerializer
)


class MarqueViewSet(viewsets.ModelViewSet):
    """ViewSet pour les marques de véhicules"""
    queryset = Marque.objects.filter(est_active=True)
    serializer_class = MarqueSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['get'])
    def modeles(self, request, pk=None):
        """Liste des modèles d'une marque"""
        marque = self.get_object()
        modeles = marque.modeles.filter(est_actif=True)
        serializer = ModeleSerializer(modeles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def statistiques(self, request, pk=None):
        """Statistiques détaillées d'une marque"""
        marque = self.get_object()
        
        # Nombre de modèles
        nombre_modeles = marque.modeles.filter(est_actif=True).count()
        
        # Répartition par catégorie
        repartition_categories = (
            marque.modeles.filter(est_actif=True)
            .values('categorie')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        # Prix moyen
        prix_moyen = marque.modeles.filter(
            est_actif=True,
            prix_occasion_moyen__isnull=False
        ).aggregate(avg_price=Avg('prix_occasion_moyen'))['avg_price']
        
        # Note de fiabilité moyenne
        fiabilite_moyenne = marque.modeles.filter(
            est_actif=True,
            indice_fiabilite__isnull=False
        ).aggregate(avg_fiabilite=Avg('indice_fiabilite'))['avg_fiabilite']
        
        return Response({
            'marque': marque.nom,
            'nombre_modeles': nombre_modeles,
            'repartition_categories': list(repartition_categories),
            'prix_moyen': float(prix_moyen) if prix_moyen else None,
            'fiabilite_moyenne': round(fiabilite_moyenne, 1) if fiabilite_moyenne else None,
            'pays_origine': marque.pays_origine,
            'annee_creation': marque.annee_creation,
        })


class ModeleViewSet(viewsets.ModelViewSet):
    """ViewSet pour les modèles de véhicules"""
    queryset = Modele.objects.filter(est_actif=True).select_related('marque')
    serializer_class = ModeleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtres
        marque_id = self.request.query_params.get('marque')
        categorie = self.request.query_params.get('categorie')
        prix_min = self.request.query_params.get('prix_min')
        prix_max = self.request.query_params.get('prix_max')
        annee_min = self.request.query_params.get('annee_min')
        carburant = self.request.query_params.get('carburant')
        
        if marque_id:
            queryset = queryset.filter(marque_id=marque_id)
        if categorie:
            queryset = queryset.filter(categorie=categorie)
        if prix_min:
            queryset = queryset.filter(prix_occasion_moyen__gte=prix_min)
        if prix_max:
            queryset = queryset.filter(prix_occasion_moyen__lte=prix_max)
        if annee_min:
            queryset = queryset.filter(annee_lancement__gte=annee_min)
        if carburant:
            queryset = queryset.filter(motorisations__type_carburant=carburant).distinct()
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def motorisations(self, request, pk=None):
        """Motorisations disponibles pour ce modèle"""
        modele = self.get_object()
        motorisations = modele.motorisations.filter(est_disponible=True)
        serializer = MotorisationSerializer(motorisations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def finitions(self, request, pk=None):
        """Finitions disponibles pour ce modèle"""
        modele = self.get_object()
        finitions = modele.finitions.all()
        serializer = FinitionSerializer(finitions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def avis_experts(self, request, pk=None):
        """Avis d'experts pour ce modèle"""
        modele = self.get_object()
        avis = modele.avis_experts.all()
        serializer = AvisExpertSerializer(avis, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def problemes_courants(self, request, pk=None):
        """Problèmes courants pour ce modèle"""
        modele = self.get_object()
        problemes = modele.problemes_courants.all()
        serializer = ProblemeCourantSerializer(problemes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def donnees_marche(self, request, pk=None):
        """Données de marché pour ce modèle"""
        modele = self.get_object()
        pays = request.query_params.get('pays', 'DZ')
        
        donnees = modele.donnees_marche.filter(pays=pays).order_by('-annee')
        serializer = DonneeMarcheSerializer(donnees, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def comparateur(self, request, pk=None):
        """Données pour le comparateur"""
        modele = self.get_object()
        
        # Comparer avec les concurrents directs
        concurrents = Modele.objects.filter(
            categorie=modele.categorie,
            est_actif=True
        ).exclude(id=modele.id).select_related('marque')[:5]
        
        data = {
            'modele_principal': ModeleSerializer(modele).data,
            'concurrents': ModeleSerializer(concurrents, many=True).data,
            'critères_comparaison': [
                'prix_occasion_moyen',
                'consommation_mixte',
                'acceleration_0_100',
                'note_euro_ncap',
                'indice_fiabilite',
                'volume_coffre',
                'nombre_places'
            ]
        }
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def recherche_avancee(self, request):
        """Recherche avancée de modèles"""
        queryset = self.get_queryset()
        
        # Critères de recherche
        recherche = request.query_params.get('recherche', '')
        categories = request.query_params.getlist('categories')
        marques = request.query_params.getlist('marques')
        prix_min = request.query_params.get('prix_min')
        prix_max = request.query_params.get('prix_max')
        annee_min = request.query_params.get('annee_min')
        annee_max = request.query_params.get('annee_max')
        
        if recherche:
            queryset = queryset.filter(
                Q(nom__icontains=recherche) |
                Q(marque__nom__icontains=recherche) |
                Q(description__icontains=recherche)
            )
        
        if categories:
            queryset = queryset.filter(categorie__in=categories)
        
        if marques:
            queryset = queryset.filter(marque_id__in=marques)
        
        if prix_min:
            queryset = queryset.filter(prix_occasion_moyen__gte=prix_min)
        if prix_max:
            queryset = queryset.filter(prix_occasion_moyen__lte=prix_max)
        
        if annee_min:
            queryset = queryset.filter(annee_lancement__gte=annee_min)
        if annee_max:
            queryset = queryset.filter(annee_lancement__lte=annee_max)
        
        # Tri
        tri = request.query_params.get('tri', 'prix_occasion_moyen')
        if tri == 'prix_asc':
            queryset = queryset.order_by('prix_occasion_moyen')
        elif tri == 'prix_desc':
            queryset = queryset.order_by('-prix_occasion_moyen')
        elif tri == 'fiabilite':
            queryset = queryset.order_by('-indice_fiabilite')
        elif tri == 'consommation':
            queryset = queryset.order_by('consommation_mixte')
        elif tri == 'annee':
            queryset = queryset.order_by('-annee_lancement')
        
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size
        
        total_count = queryset.count()
        modeles = queryset[start:end]
        
        serializer = self.get_serializer(modeles, many=True)
        
        return Response({
            'resultats': serializer.data,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': (total_count + page_size - 1) // page_size,
            },
            'filtres_appliques': {
                'recherche': recherche,
                'categories': categories,
                'marques': marques,
                'prix_min': prix_min,
                'prix_max': prix_max,
                'annee_min': annee_min,
                'annee_max': annee_max,
            }
        })


class MotorisationViewSet(viewsets.ModelViewSet):
    """ViewSet pour les motorisations"""
    queryset = Motorisation.objects.filter(est_disponible=True).select_related('modele')
    serializer_class = MotorisationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        modele_id = self.request.query_params.get('modele')
        carburant = self.request.query_params.get('carburant')
        puissance_min = self.request.query_params.get('puissance_min')
        
        if modele_id:
            queryset = queryset.filter(modele_id=modele_id)
        if carburant:
            queryset = queryset.filter(type_carburant=carburant)
        if puissance_min:
            queryset = queryset.filter(puissance__gte=puissance_min)
        
        return queryset


class FinitionViewSet(viewsets.ModelViewSet):
    """ViewSet pour les finitions"""
    queryset = Finition.objects.all().select_related('modele')
    serializer_class = FinitionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EquipementViewSet(viewsets.ModelViewSet):
    """ViewSet pour les équipements"""
    queryset = Equipement.objects.all()
    serializer_class = EquipementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        categorie = self.request.query_params.get('categorie')
        
        if categorie:
            queryset = queryset.filter(categorie=categorie)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Liste des catégories d'équipements"""
        categories = Equipement.objects.values_list('categorie', flat=True).distinct()
        return Response(list(categories))


class AvisExpertViewSet(viewsets.ModelViewSet):
    """ViewSet pour les avis d'experts"""
    queryset = AvisExpert.objects.all().select_related('modele', 'modele__marque')
    serializer_class = AvisExpertSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        modele_id = self.request.query_params.get('modele')
        source = self.request.query_params.get('source')
        note_min = self.request.query_params.get('note_min')
        
        if modele_id:
            queryset = queryset.filter(modele_id=modele_id)
        if source:
            queryset = queryset.filter(source__icontains=source)
        if note_min:
            queryset = queryset.filter(note_globale__gte=note_min)
        
        return queryset


class ProblemeCourantViewSet(viewsets.ModelViewSet):
    """ViewSet pour les problèmes courants"""
    queryset = ProblemeCourant.objects.all().select_related('modele', 'modele__marque')
    serializer_class = ProblemeCourantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        modele_id = self.request.query_params.get('modele')
        gravite_min = self.request.query_params.get('gravite_min')
        
        if modele_id:
            queryset = queryset.filter(modele_id=modele_id)
        if gravite_min:
            queryset = queryset.filter(gravite__gte=gravite_min)
        
        return queryset.order_by('-gravite', '-frequence_apparition')


class DonneeMarcheViewSet(viewsets.ModelViewSet):
    """ViewSet pour les données de marché"""
    queryset = DonneeMarche.objects.all().select_related('modele', 'modele__marque')
    serializer_class = DonneeMarcheSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        modele_id = self.request.query_params.get('modele')
        pays = self.request.query_params.get('pays', 'DZ')
        annee = self.request.query_params.get('annee')
        
        if modele_id:
            queryset = queryset.filter(modele_id=modele_id)
        if pays:
            queryset = queryset.filter(pays=pays)
        if annee:
            queryset = queryset.filter(annee=annee)
        
        return queryset.order_by('-annee')


class BibliothequeViewSet(viewsets.GenericViewSet):
    """ViewSet pour les fonctionnalités globales de la bibliothèque"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def statistiques_globales(self, request):
        """Statistiques globales de la bibliothèque"""
        stats = {
            'total_marques': Marque.objects.filter(est_active=True).count(),
            'total_modeles': Modele.objects.filter(est_actif=True).count(),
            'total_motorisations': Motorisation.objects.filter(est_disponible=True).count(),
            'total_avis_experts': AvisExpert.objects.count(),
            'total_problemes': ProblemeCourant.objects.count(),
        }
        
        # Répartition par catégorie
        repartition_categories = (
            Modele.objects.filter(est_actif=True)
            .values('categorie')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        # Top 10 des marques par nombre de modèles
        top_marques = (
            Marque.objects.filter(est_active=True)
            .annotate(nombre_modeles=Count('modeles'))
            .order_by('-nombre_modeles')[:10]
        )
        
        # Prix moyen par catégorie
        prix_par_categorie = (
            Modele.objects.filter(
                est_actif=True,
                prix_occasion_moyen__isnull=False
            ).values('categorie')
            .annotate(prix_moyen=Avg('prix_occasion_moyen'))
            .order_by('prix_moyen')
        )
        
        return Response({
            'stats_generales': stats,
            'repartition_categories': list(repartition_categories),
            'top_marques': [
                {
                    'nom': marque.nom,
                    'nombre_modeles': marque.nombre_modeles,
                    'pays_origine': marque.pays_origine
                }
                for marque in top_marques
            ],
            'prix_par_categorie': list(prix_par_categorie)
        })
    
    @action(detail=False, methods=['get'])
    def suggestions_recherche(self, request):
        """Suggestions pour la recherche de véhicules"""
        terme = request.query_params.get('q', '')
        
        if len(terme) < 2:
            return Response({'suggestions': []})
        
        # Suggestions de marques
        marques = Marque.objects.filter(
            nom__icontains=terme,
            est_active=True
        ).values_list('nom', flat=True)[:5]
        
        # Suggestions de modèles
        modeles = Modele.objects.filter(
            Q(nom__icontains=terme) | Q(marque__nom__icontains=terme),
            est_actif=True
        ).select_related('marque')[:10]
        
        modeles_suggestions = [
            {
                'id': modele.id,
                'nom_complet': modele.nom_complet,
                'marque': modele.marque.nom,
                'categorie': modele.categorie,
                'prix_moyen': float(modele.prix_occasion_moyen) if modele.prix_occasion_moyen else None
            }
            for modele in modeles
        ]
        
        return Response({
            'marques': list(marques),
            'modeles': modeles_suggestions
        })
    
    @action(detail=False, methods=['get'])
    def export_donnees(self, request):
        """Export des données de la bibliothèque"""
        format_export = request.query_params.get('format', 'json')
        modele_id = request.query_params.get('modele')
        
        if modele_id:
            modele = get_object_or_404(Modele, id=modele_id)
            data = {
                'modele': ModeleSerializer(modele).data,
                'motorisations': MotorisationSerializer(
                    modele.motorisations.all(), many=True
                ).data,
                'finitions': FinitionSerializer(
                    modele.finitions.all(), many=True
                ).data,
                'avis_experts': AvisExpertSerializer(
                    modele.avis_experts.all(), many=True
                ).data,
                'problemes': ProblemeCourantSerializer(
                    modele.problemes_courants.all(), many=True
                ).data,
                'donnees_marche': DonneeMarcheSerializer(
                    modele.donnees_marche.all(), many=True
                ).data,
            }
        else:
            # Export de toute la bibliothèque
            data = {
                'marques': MarqueSerializer(
                    Marque.objects.filter(est_active=True), many=True
                ).data,
                'modeles': ModeleSerializer(
                    Modele.objects.filter(est_actif=True), many=True
                ).data,
            }
        
        if format_export == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="bibliotheque_vehicules.csv"'
            
            writer = csv.writer(response)
            if modele_id:
                writer.writerow(['Modèle', 'Marque', 'Catégorie', 'Prix moyen', 'Fiabilité'])
                modele = data['modele']
                writer.writerow([
                    modele['nom'],
                    modele['marque']['nom'],
                    modele['categorie'],
                    modele['prix_occasion_moyen'],
                    modele['indice_fiabilite']
                ])
            else:
                writer.writerow(['Marque', 'Nombre de modèles'])
                for marque in data['marques']:
                    writer.writerow([marque['nom'], len(Modele.objects.filter(marque_id=marque['id']))])
            
            return response
        else:
            response = HttpResponse(
                json.dumps(data, indent=2, default=str),
                content_type='application/json'
            )
            response['Content-Disposition'] = 'attachment; filename="bibliotheque_vehicules.json"'
            return response
