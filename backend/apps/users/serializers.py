from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value.lower()

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password2": "Les mots de passe ne correspondent pas."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


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
