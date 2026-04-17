import csv
from django.http import HttpResponse
from django.db.models import Avg, Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.permissions import IsPlanPro
from .models import Annonce, Marque
from .serializers import (
    AnnonceListSerializer, AnnonceDetailSerializer, MarqueSerializer
)
from .filters import AnnonceFilter


class MarqueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Marque.objects.all()
    serializer_class = MarqueSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'slug']


class AnnonceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter
    ]
    filterset_class = AnnonceFilter
    search_fields = ['marque__nom', 'modele', 'ville']
    ordering_fields = [
        'prix', 'date_publication', 'kilometrage',
        'score_affaire', 'ecart_prix'
    ]
    ordering = ['-date_publication']

    def get_queryset(self):
        return Annonce.objects.filter(
            est_active=True
        ).select_related('marque').defer(
            'description', 'url_originale', 'source'
        )

    def get_serializer_class(self):
        return (
            AnnonceDetailSerializer if self.action == 'retrieve'
            else AnnonceListSerializer
        )

    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(60 * 5))
    def bonnes_affaires(self, request):
        qs = self.get_queryset().filter(
            est_bonne_affaire=True
        ).order_by('ecart_prix')[:20]
        return Response(AnnonceListSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(60 * 10))
    def stats_marques(self, request):
        pays = request.query_params.get('pays', 'DZ')
        data = self.get_queryset().filter(pays=pays).values(
            'marque__nom', 'marque__slug'
        ).annotate(
            nb=Count('id'), prix_moyen=Avg('prix'),
            bonnes_affaires=Count('id', filter=Q(est_bonne_affaire=True))
        ).order_by('-nb')[:15]
        return Response(list(data))

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        if not IsPlanPro().has_permission(request, self):
            return Response(
                {'error': True, 'message': 'Export CSV Pro uniquement.'},
                status=403
            )
        qs = self.filter_queryset(self.get_queryset())[:1000]
        response = HttpResponse(
            content_type='text/csv; charset=utf-8'
        )
        response['Content-Disposition'] = (
            'attachment; filename="autointel_annonces.csv"'
        )
        response.write('\ufeff')
        writer = csv.writer(response, delimiter=';')
        writer.writerow([
            'Marque', 'Modèle', 'Année', 'Km', 'Prix DA',
            'Prix estimé', 'Écart%', 'Bonne affaire',
            'Carburant', 'Ville', 'Pays'
        ])
        for a in qs:
            writer.writerow([
                a.marque.nom, a.modele, a.annee, a.kilometrage,
                a.prix, a.prix_estime or '',
                f"{a.ecart_prix:.1f}" if a.ecart_prix else '',
                'Oui' if a.est_bonne_affaire else 'Non',
                a.carburant, a.ville, a.pays,
            ])
        return response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_favori(self, request, pk=None):
        """Ajoute/Retire une annonce des favoris de l'utilisateur."""
        annonce = self.get_object()
        favori, created = Favori.objects.get_or_create(user=request.user, annonce=annonce)
        
        if not created:
            favori.delete()
            return Response({'status': 'removed', 'message': 'Retiré des favoris'}, status=status.HTTP_200_OK)
        
        return Response({'status': 'added', 'message': 'Ajouté aux favoris'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def similaires(self, request, pk=None):
        """Trouve des annonces similaires (même marque, même carburant, prix ±30%)."""
        annonce = self.get_object()
        prix_min = float(annonce.prix) * 0.7
        prix_max = float(annonce.prix) * 1.3
        
        similaires = Annonce.objects.filter(
            vehicule__marque=annonce.vehicule.marque,
            carburant=annonce.carburant,
            prix__gte=prix_min,
            prix__lte=prix_max
        ).exclude(id=annonce.id)[:6]
        
        serializer = self.get_serializer(similaires, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def bonnes_affaires(self, request):
        """Retourne les bonnes affaires triées par écart prix"""
        queryset = self.get_queryset().filter(est_bonne_affaire=True)
        queryset = queryset.order_by('ecart_prix')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats_marque(self, request):
        """Stats par marque : avg prix, count, min, max"""
        stats = list(
            self.get_queryset()
            .values('vehicule__marque')
            .annotate(
                count=Count('id'),
                prix_moyen=Avg('prix'),
                prix_min=Min('prix'),
                prix_max=Max('prix'),
            )
            .order_by('-count')[:10]
        )
        return Response(stats)

    @action(detail=False, methods=['get'])
    def par_pays(self, request):
        """Compte les annonces par pays"""
        stats = list(
            self.get_queryset()
            .values('pays')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        return Response(stats)

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        abonnement = getattr(request.user, 'subscription', None)
        plan_nom = abonnement.plan.nom if abonnement else None
        if plan_nom not in ['pro', 'business']:
            return Response(
                {'error': 'Export CSV disponible uniquement en plan Pro ou Business'},
                status=status.HTTP_403_FORBIDDEN)

        annonces = self.filter_queryset(self.get_queryset())[:1000]

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="autointel_annonces.csv"'
        response.write('\ufeff')  # BOM pour compatibilité Excel

        writer = csv.writer(response, delimiter=';')
        writer.writerow([
            'Marque', 'Modèle', 'Année', 'Kilométrage',
            'Carburant', 'Boîte', 'Prix (DA/€)', 'Prix estimé',
            'Écart %', 'Bonne affaire', 'Ville', 'Pays',
            'Date publication'
        ])

        for a in annonces:
            writer.writerow([
                a.vehicule.marque,
                a.vehicule.modele,
                a.annee,
                a.kilometrage,
                a.carburant,
                a.boite,
                a.prix,
                a.prix_estime or 'N/A',
                f"{a.ecart_prix:.1f}%" if a.ecart_prix else 'N/A',
                'Oui' if a.est_bonne_affaire else 'Non',
                a.ville or 'N/A',
                a.pays,
                a.date_publication.strftime('%d/%m/%Y') if a.date_publication else 'N/A'
            ])

        return response


                        
        return Response({'status': 'vote enregistré', 'votes_v1': battle.votes_v1, 'votes_v2': battle.votes_v2})

    @action(detail=False, methods=['get'])
    def versus(self, request):
        v1_id = request.query_params.get('v1')
        v2_id = request.query_params.get('v2')
        
        if not v1_id or not v2_id:
            return Response({'detail': 'Deux IDs sont requis (v1, v2)'}, status=status.HTTP_400_BAD_REQUEST)
            
        v1 = get_object_or_404(Annonce, id=v1_id)
        v2 = get_object_or_404(Annonce, id=v2_id)
        
        serializer_v1 = AnnonceSerializer(v1)
        serializer_v2 = AnnonceSerializer(v2)
        
        return Response({
            'v1': serializer_v1.data,
            'v2': serializer_v2.data,
            'verdict': 'v1' if v1.score_affaire > v2.score_affaire else 'v2' if v2.score_affaire > v1.score_affaire else 'egalite'
        })
