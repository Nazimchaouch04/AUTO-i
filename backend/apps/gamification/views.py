from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from .models import ProfilJoueur, Transaction, DefiJoueur, Defi
from .serializers import ProfilJoueurSerializer, TransactionSerializer, DefiJoueurSerializer


class ProfilJoueurViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def profil(self, request):
        profil = request.user.profil
        serializer = ProfilJoueurSerializer(profil)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_coins(self, request):
        amount = request.data.get('amount', 0)
        reason = request.data.get('reason', 'Manual addition')

        profil = request.user.profil
        profil.add_coins(amount)

        # Crée une transaction
        Transaction.objects.create(
            profil=profil,
            montant=amount,
            type='gain_estimation',
            description=reason
        )

        return Response({'detail': f'{amount} AutoCoins ajoutés', 'balance': profil.autocoin_balance})

    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        type_lb = request.query_params.get('type', 'global')
        limit = int(request.query_params.get('limit', 10))

        if type_lb == 'xp':
            profiles = ProfilJoueur.objects.all().order_by('-xp')[:limit]
        elif type_lb == 'coins':
            profiles = ProfilJoueur.objects.all().order_by('-autocoin_balance')[:limit]
        else:  # global
            profiles = ProfilJoueur.objects.all().order_by('-niveau', '-xp')[:limit]

        serializer = ProfilJoueurSerializer(profiles, many=True)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def list(self, request):
        profil = request.user.profil
        transactions = profil.transactions.all()[:20]
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class DefiViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def list(self, request):
        defis = Defi.objects.filter(is_active=True)
        profil = request.user.profil

        # Récupère les défis en cours de l'utilisateur
        defis_en_cours = DefiJoueur.objects.filter(profil=profil, completed=False).values_list('defi_id', flat=True)

        response_data = []
        for defi in defis:
            defi_joueur = DefiJoueur.objects.filter(profil=profil, defi=defi).first()
            data = {
                'id': defi.id,
                'titre': defi.titre,
                'description': defi.description,
                'type': defi.get_type_display(),
                'xp_reward': defi.xp_reward,
                'ac_reward': defi.ac_reward,
                'cible_count': defi.cible_count,
                'en_cours': defi.id in defis_en_cours,
                'progression': defi_joueur.progression if defi_joueur else 0,
                'completed': defi_joueur.completed if defi_joueur else False,
            }
            response_data.append(data)

        return Response(response_data)
