from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Q
from .models import Vehicule, Annonce
from .serializers import VehiculeSerializer, AnnonceSerializer


class VehiculeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['marque', 'modele']


class AnnonceViewSet(viewsets.ModelViewSet):
    queryset = Annonce.objects.select_related('vehicule').all()
    serializer_class = AnnonceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'vehicule__marque': ['exact', 'icontains'],
        'prix': ['gte', 'lte'],
        'kilometrage': ['lte'],
        'annee': ['gte', 'lte'],
        'carburant': ['exact'],
        'pays': ['exact'],
        'est_bonne_affaire': ['exact'],
    }
    search_fields = ['vehicule__marque', 'vehicule__modele', 'ville', 'description']
    ordering_fields = ['prix', 'annee', 'kilometrage', 'date_publication']
    ordering = ['-date_publication']

    @action(detail=False, methods=['get'])
    def bonnes_affaires(self, request):
        """Retourne les bonnes affaires triées par écart prix"""
        queryset = self.get_queryset().filter(est_bonne_affaire=True)
        queryset = queryset.order_by('ecart_prix')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats_marque(self, request):
        """Stats par marque : avg prix, count, min, max"""
        stats = list(
            self.get_queryset()
            .values('vehicule__marque')
            .annotate(
                marque=Count('id'),
                count=Count('id'),
                prix_moyen=Avg('prix'),
                prix_min=Avg('prix'),
                prix_max=Avg('prix'),
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
