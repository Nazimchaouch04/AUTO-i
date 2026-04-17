import csv
from django.http import HttpResponse
from django.db.models import Avg, Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
