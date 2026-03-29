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
    annee = serializers.IntegerField(required=False)
    annee_min = serializers.IntegerField(required=False)
    annee_max = serializers.IntegerField(required=False)
    kilometrage = serializers.IntegerField()
    carburant = serializers.CharField(max_length=20)
    boite = serializers.CharField(max_length=20, required=False)
    puissance = serializers.IntegerField(required=False, allow_null=True)
    pays = serializers.CharField(max_length=5, default='DZ')

    def validate(self, attrs):
        annee = attrs.get('annee')
        annee_min = attrs.get('annee_min')
        annee_max = attrs.get('annee_max')

        if annee is None and (annee_min is None or annee_max is None):
            raise serializers.ValidationError(
                "Vous devez fournir 'annee' ou ('annee_min' et 'annee_max')."
            )

        if annee_min is not None and annee_max is not None and annee_min > annee_max:
            raise serializers.ValidationError("'annee_min' doit être <= 'annee_max'.")

        return attrs
