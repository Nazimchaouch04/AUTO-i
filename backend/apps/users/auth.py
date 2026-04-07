from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Supporte la connexion avec email OU nom d'utilisateur.
    """

    email = serializers.CharField(required=False, allow_blank=False)
    username = serializers.CharField(required=False, allow_blank=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Le serializer JWT natif rend "username" obligatoire par defaut.
        # On le passe en optionnel pour accepter aussi "email".
        self.fields[self.username_field].required = False

    def validate(self, attrs):
        login_input = attrs.get("email") or attrs.get("username")
        if not login_input:
            raise AuthenticationFailed("Email ou nom d'utilisateur requis.")

        # Si l'utilisateur saisit un email, on retrouve son username Django.
        if "@" in login_input:
            user = User.objects.filter(email__iexact=login_input).first()
            attrs[self.username_field] = user.get_username() if user else login_input
        else:
            attrs[self.username_field] = login_input

        data = super().validate(attrs)
        data["user_data"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        }
        return data


class EmailOrUsernameTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailOrUsernameTokenObtainPairSerializer
