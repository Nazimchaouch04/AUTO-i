from rest_framework import serializers
from .models import Vehicule, Annonce


class VehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicule
        fields = ['id', 'marque', 'modele', 'categorie']


class AnnonceSerializer(serializers.ModelSerializer):
    vehicule_marque = serializers.CharField(source='vehicule.marque', read_only=True)
    vehicule_modele = serializers.CharField(source='vehicule.modele', read_only=True)
    prix_display = serializers.SerializerMethodField()
    ecart_pct_display = serializers.SerializerMethodField()
    badge_type = serializers.SerializerMethodField()

    class Meta:
        model = Annonce
        fields = [
            'id', 'vehicule', 'vehicule_marque', 'vehicule_modele', 'annee', 'kilometrage',
            'carburant', 'boite', 'puissance', 'prix', 'prix_display', 'prix_estime',
            'ecart_prix', 'ecart_pct_display', 'score_affaire', 'est_bonne_affaire',
            'badge_type', 'source', 'url_originale', 'ville', 'pays', 'description',
            'date_publication', 'est_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'date_publication', 'created_at', 'updated_at']

    def get_prix_display(self, obj):
        return f"{obj.prix:,.0f}€"

    def get_ecart_pct_display(self, obj):
        if obj.prix_estime and obj.prix:
            return round((float(obj.prix_estime) - float(obj.prix)) / float(obj.prix_estime) * 100, 1)
        return None

    def get_badge_type(self, obj):
        if obj.est_bonne_affaire:
            if obj.ecart_prix and obj.ecart_prix < -15:
                return 'excellent'
            return 'bonne'
        return None
