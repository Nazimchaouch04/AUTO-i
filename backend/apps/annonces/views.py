from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Min, Max, Q
from django.shortcuts import get_object_or_404
from .models import Vehicule, Annonce, Favori, RechercheSauvegardee, Battle
from .serializers import VehiculeSerializer, AnnonceSerializer, RechercheSauvegardeeSerializer, BattleSerializer


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
        'vehicule__modele': ['exact', 'icontains'],
        'prix': ['gte', 'lte'],
        'kilometrage': ['gte', 'lte'],
        'annee': ['gte', 'lte'],
        'carburant': ['exact'],
        'boite': ['exact'],
        'pays': ['exact'],
        'ville': ['icontains'],
        'est_bonne_affaire': ['exact'],
    }
    search_fields = ['vehicule__marque', 'vehicule__modele', 'ville', 'description']
    ordering_fields = ['prix', 'annee', 'kilometrage', 'date_publication', 'ecart_prix']
    ordering = ['-date_publication']

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mes_favoris(self, request):
        """Retourne les annonces favorites de l'utilisateur connecté."""
        favoris_ids = Favori.objects.filter(user=request.user).values_list('annonce_id', flat=True)
        queryset = self.get_queryset().filter(id__in=favoris_ids)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
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


class RechercheSauvegardeeViewSet(viewsets.ModelViewSet):
    serializer_class = RechercheSauvegardeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RechercheSauvegardee.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        recherche = serializer.save(user=self.request.user)
        # Gain d'XP pour la sauvegarde
        if hasattr(self.request.user, 'profil'):
            self.request.user.profil.add_xp(10)


class BattleViewSet(viewsets.ModelViewSet):
    queryset = Battle.objects.select_related('vehicule_1__vehicule', 'vehicule_2__vehicule', 'createur').all()
    serializer_class = BattleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(createur=self.request.user)
        # Gain XP pour création de battle
        if hasattr(self.request.user, 'profil'):
            self.request.user.profil.add_xp(50)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        battle = self.get_object()
        vehicule_id = request.data.get('vehicule_id')
        
        if not vehicule_id:
            return Response({'detail': 'ID véhicule requis'}, status=status.HTTP_400_BAD_REQUEST)
        
        if int(vehicule_id) == battle.vehicule_1.id:
            battle.votes_v1 += 1
        elif int(vehicule_id) == battle.vehicule_2.id:
            battle.votes_v2 += 1
        else:
            return Response({'detail': 'Véhicule invalide pour cette battle'}, status=status.HTTP_400_BAD_REQUEST)
        
        battle.save()
        # Gain AC pour avoir voté
        if hasattr(request.user, 'profil'):
            request.user.profil.add_coins(5)
            
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
