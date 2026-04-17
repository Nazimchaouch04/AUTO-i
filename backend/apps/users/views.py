from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserProfileSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        profile = user.profile
        profile.add_coins(100)   # bonus inscription
        profile.add_xp(50)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id, 'username': user.username,
                'email': user.email
            },
            'profil': UserProfileSerializer(profile).data,
            'message': '🎉 Bienvenue ! +100 AutoCoins offerts !',
        }, status=status.HTTP_201_CREATED)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            UserProfileSerializer(request.user.profile).data
        )

    def patch(self, request):
        serializer = UserProfileSerializer(
            request.user.profile,
            data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_pw = request.data.get('old_password', '')
        new_pw = request.data.get('new_password', '')
        if not user.check_password(old_pw):
            return Response(
                {'error': True, 'message': 'Mot de passe actuel incorrect.'},
                status=400
            )
        if len(new_pw) < 6:
            return Response(
                {'error': True, 'message': 'Minimum 6 caractères.'},
                status=400
            )
        user.set_password(new_pw)
        user.save()
        return Response({'message': 'Mot de passe modifié.'})
