from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.alertes.models import Alerte
from apps.annonces.models import Favori, RechercheSauvegardee
from apps.gamification.models import ProfilJoueur
from apps.subscriptions.models import Abonnement

from .models import UserProfile
from .serializers import RegisterSerializer, UserProfileSerializer


class RegisterView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'detail': "Inscription reussie. 100 AutoCoins offerts a l'inscription !",
                'message': "Inscription reussie. 100 AutoCoins offerts a l'inscription !",
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'profil_data': self._build_gamification_data(user),
                'abonnement_data': self._build_subscription_data(user),
            },
            status=status.HTTP_201_CREATED,
        )

    def _build_gamification_data(self, user):
        profil, _ = ProfilJoueur.objects.get_or_create(user=user)
        return {
            'xp': profil.xp,
            'niveau': profil.niveau,
            'autocoin_balance': profil.autocoin_balance,
            'nom_niveau': profil.nom_niveau(),
            'progression_pct': profil.progression_pct(),
        }

    def _build_subscription_data(self, user):
        abonnement = Abonnement.objects.filter(user=user, actif=True).select_related('plan').first()
        if not abonnement:
            return {}

        return {
            'plan_nom': abonnement.plan.get_nom_display(),
            'estimations_restantes': abonnement.plan.estimations_par_mois,
            'alertes_max': abonnement.plan.alertes_max,
            'export_csv': abonnement.plan.export_csv,
        }


class UserProfileView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'put'])
    def profile(self, request):
        user_profile = self._get_or_create_user_profile(request.user)

        if request.method == 'PUT':
            user_field_errors = self._update_user_identity(request.user, request.data)
            if user_field_errors:
                return Response(user_field_errors, status=status.HTTP_400_BAD_REQUEST)

            serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return self._get_full_profile_response(request.user)

    def _get_or_create_user_profile(self, user):
        initials = (user.username[:2] or 'AI').upper()
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'avatar_initials': initials},
        )

        if not profile.avatar_initials:
            profile.avatar_initials = initials
            profile.save(update_fields=['avatar_initials'])

        return profile

    def _update_user_identity(self, user, payload):
        errors = {}

        raw_username = payload.get('username')
        raw_email = payload.get('email')

        if raw_username is not None:
            username = str(raw_username).strip()
            if not username:
                errors['username'] = ["Le nom d'utilisateur ne peut pas etre vide."]
            elif User.objects.filter(username__iexact=username).exclude(pk=user.pk).exists():
                errors['username'] = ["Ce nom d'utilisateur est deja utilise."]
            else:
                user.username = username

        if raw_email is not None:
            email = str(raw_email).strip().lower()
            if not email:
                errors['email'] = ["L'email ne peut pas etre vide."]
            elif User.objects.filter(email__iexact=email).exclude(pk=user.pk).exists():
                errors['email'] = ['Cet email est deja utilise.']
            else:
                user.email = email

        if errors:
            return errors

        if raw_username is not None or raw_email is not None:
            user.save(update_fields=['username', 'email'])

        return None

    def _get_full_profile_response(self, user):
        profil_joueur, _ = ProfilJoueur.objects.get_or_create(user=user)

        abonnement = Abonnement.objects.filter(user=user, actif=True).select_related('plan').first()
        if abonnement:
            abonnement_data = {
                'plan_nom': abonnement.plan.get_nom_display(),
                'estimations_restantes': abonnement.plan.estimations_par_mois,
                'alertes_max': abonnement.plan.alertes_max,
                'export_csv': abonnement.plan.export_csv,
            }
        else:
            abonnement_data = {}

        favoris_count = Favori.objects.filter(user=user).count()
        recherches_count = RechercheSauvegardee.objects.filter(user=user).count()
        alertes_count = Alerte.objects.filter(user=user, est_active=True).count()

        xp = profil_joueur.xp
        medailles = []
        if xp >= 500:
            medailles.append({'type': 'bronze', 'nom': 'Bronze'})
        if xp >= 2000:
            medailles.append({'type': 'silver', 'nom': 'Silver'})
        if xp >= 5000:
            medailles.append({'type': 'gold', 'nom': 'Gold'})

        return Response(
            {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'profil': {
                    'xp': profil_joueur.xp,
                    'niveau': profil_joueur.niveau,
                    'autocoin_balance': profil_joueur.autocoin_balance,
                    'nom_niveau': profil_joueur.nom_niveau(),
                    'progression_pct': profil_joueur.progression_pct(),
                },
                'abonnement': abonnement_data,
                'stats': {
                    'favoris_count': favoris_count,
                    'recherches_count': recherches_count,
                    'alertes_count': alertes_count,
                },
                'medailles': medailles,
            }
        )
