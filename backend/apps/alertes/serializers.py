from rest_framework import serializers
from .models import Alerte


class AlerteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerte
        fields = [
            'id', 'titre', 'marque', 'modele', 'prix_max', 'km_max',
            'carburant', 'pays', 'email_actif', 'est_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
