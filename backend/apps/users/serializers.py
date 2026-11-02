from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Cet email est deja utilise.")
        return value.lower()

    def validate(self, data):
        password = data.get('password', '')
        password_confirm = data.get('password_confirm', password)
        if not (password == password_confirm):
            raise serializers.ValidationError(
                {'password': 'Les mots de passe ne correspondent pas.'}
            )
        username = data.get('username', '')
        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError(
                {'username': "Ce nom d'utilisateur est deja pris."}
            )
        data.pop('password_confirm', None)
        return data

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    plan = serializers.ReadOnlyField()
    level_name = serializers.ReadOnlyField()
    can_estimate = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = [
            'username', 'email', 'country', 'phone',
            'telegram_chat_id', 'whatsapp_number',
            'estimations_this_month', 'total_estimations',
            'last_active', 'xp', 'level', 'xp_pct', 'coins',
            'plan', 'level_name', 'can_estimate',
        ]
        read_only_fields = [
            'estimations_this_month', 'total_estimations',
            'last_active', 'xp', 'level', 'xp_pct', 'coins',
        ]
