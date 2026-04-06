from rest_framework import serializers
from .models import Alerte


class AlerteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerte
        fields = [
            'id', 'titre', 'marque', 'modele', 'prix_min', 'prix_max',
            'km_max', 'annee_min', 'carburant', 'boite_vitesse', 'pays',
            'email_actif', 'push_actif', 'est_active', 'created_at', 'last_triggered'
        ]
        read_only_fields = ['id', 'created_at']
