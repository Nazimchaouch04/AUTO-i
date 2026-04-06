from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from .serializers import UserProfileSerializer, RegisterSerializer
from apps.gamification.models import ProfilJoueur
from apps.subscriptions.models import Abonnement
from apps.annonces.models import Favori, RechercheSauvegardee


class RegisterView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Génération des tokens JWT
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    'detail': '100 AutoCoins offerts à l\'inscription !',
                    'message': '100 AutoCoins offerts à l\'inscription !',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user_data': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    },
                    'profil_data': {
                        'xp': 0,
                        'niveau': 1,
                        'autocoin_balance': 100,
                        'nom_niveau': 'Apprenti Mécanicien',
                        'progression_pct': 0
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'put'])
    def profile(self, request):
        user_profile = request.user.profile

        if request.method == 'PUT':
            serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                user = request.user
                username = request.data.get('username')
                email = request.data.get('email')
                
                # Mise à jour du modèle User
                if username:
                    user.username = username
                if email:
                    user.email = email
                if username or email:
                    user.save()

                serializer.save()
                return self._get_full_profile_response(request.user)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return self._get_full_profile_response(request.user)

    def _get_full_profile_response(self, user):
        try:
            profil_joueur = ProfilJoueur.objects.get(user=user)
            profil_data = {
                'xp': profil_joueur.xp,
                'niveau': profil_joueur.niveau,
                'autocoin_balance': profil_joueur.autocoin_balance,
                'nom_niveau': profil_joueur.nom_niveau(),
                'progression_pct': profil_joueur.progression_pct()
            }
        except Exception:
            profil_data = {}

        try:
            abonnement = Abonnement.objects.get(user=user, actif=True)
            abonnement_data = {
                'plan_nom': abonnement.plan.get_nom_display(),
                'estimations_restantes': abonnement.plan.estimations_par_mois,
                'alertes_max': abonnement.plan.alertes_max,
                'export_csv': abonnement.plan.export_csv
            }
        except Exception:
            abonnement_data = {}

        favoris_count = Favori.objects.filter(user=user).count()
        recherches_count = RechercheSauvegardee.objects.filter(user=user).count()

        # Calcul médailles (Exemple logique)
        xp = profil_data.get('xp', 0)
        medailles = []
        if xp >= 500: medailles.append({'type': 'bronze', 'nom': 'Bronze'})
        if xp >= 2000: medailles.append({'type': 'silver', 'nom': 'Silver'})
        if xp >= 5000: medailles.append({'type': 'gold', 'nom': 'Gold'})

        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'profil': profil_data,
            'abonnement': abonnement_data,
            'stats': {
                'favoris_count': favoris_count,
                'recherches_count': recherches_count,
            },
            'medailles': medailles
        })
