from rest_framework import serializers
from .models import EstimationHistory


class EstimationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EstimationHistory
        fields = [
            'id', 'marque', 'modele', 'annee', 'kilometrage', 'carburant',
            'boite', 'puissance', 'pays', 'prix_estime', 'fourchette_basse',
            'fourchette_haute', 'fiabilite', 'nb_annonces_reference', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class EstimationRequestSerializer(serializers.Serializer):
    marque = serializers.CharField(max_length=100)
    modele = serializers.CharField(max_length=100)
    annee = serializers.IntegerField()
    kilometrage = serializers.IntegerField()
    carburant = serializers.CharField(max_length=20)
    boite = serializers.CharField(max_length=20, required=False)
    puissance = serializers.IntegerField(required=False, allow_null=True)
    pays = serializers.CharField(max_length=5, default='DZ')
