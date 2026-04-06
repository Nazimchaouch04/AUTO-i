from rest_framework import serializers
from .models import Vehicule, Annonce, RechercheSauvegardee, Battle


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
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Annonce
        fields = [
            'id', 'vehicule', 'vehicule_marque', 'vehicule_modele', 'annee', 'kilometrage',
            'carburant', 'boite', 'puissance', 'prix', 'prix_display', 'prix_estime',
            'ecart_prix', 'ecart_pct_display', 'score_affaire', 'est_bonne_affaire',
            'badge_type', 'is_favorite', 'source', 'url_originale', 'ville', 'pays', 'description',
            'date_publication', 'est_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'date_publication', 'created_at', 'updated_at']

    def get_prix_display(self, obj):
        return f"{obj.prix:,.0f}€"

    def get_ecart_pct_display(self, obj):
        if obj.prix_estime and obj.prix:
            val = float((float(obj.prix_estime) - float(obj.prix)) / float(obj.prix_estime) * 100)
            return float(f"{val:.1f}")
        return None

    def get_badge_type(self, obj):
        if obj.est_bonne_affaire:
            if obj.ecart_prix and (float(obj.ecart_prix) < -15):
                return 'excellent'
            return 'bonne'
        return None

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favoris_selectionnes.filter(user=request.user).exists()
        return False


class BattleSerializer(serializers.ModelSerializer):
    vehicule_1_details = AnnonceSerializer(source='vehicule_1', read_only=True)
    vehicule_2_details = AnnonceSerializer(source='vehicule_2', read_only=True)
    createur_username = serializers.CharField(source='createur.username', read_only=True)
    winner_id = serializers.SerializerMethodField()

    class Meta:
        model = Battle
        fields = [
            'id', 'vehicule_1', 'vehicule_2', 'vehicule_1_details', 'vehicule_2_details',
            'createur', 'createur_username', 'votes_v1', 'votes_v2', 'titre',
            'description', 'is_active', 'winner_id', 'created_at'
        ]
        read_only_fields = ['id', 'votes_v1', 'votes_v2', 'createur', 'is_active', 'created_at']

    def get_winner_id(self, obj):
        return obj.calculate_winner()


class RechercheSauvegardeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RechercheSauvegardee
        fields = ['id', 'user', 'nom', 'query_params', 'result_count', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
