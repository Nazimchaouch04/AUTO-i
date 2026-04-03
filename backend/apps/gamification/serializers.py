from rest_framework import serializers
from .models import ProfilJoueur, Transaction, Defi, DefiJoueur, BoutiqueItem, AchatJoueur


class BoutiqueItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoutiqueItem
        fields = ['id', 'nom', 'description', 'prix_ac', 'image_url', 'slug', 'created_at']


class AchatJoueurSerializer(serializers.ModelSerializer):
    item_details = BoutiqueItemSerializer(source='item', read_only=True)

    class Meta:
        model = AchatJoueur
        fields = ['id', 'item', 'item_details', 'date_achat']
        read_only_fields = ['id', 'date_achat', 'item_details']


class ProfilJoueurSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    nom_niveau_display = serializers.SerializerMethodField()
    progression_pct = serializers.SerializerMethodField()

    class Meta:
        model = ProfilJoueur
        fields = [
            'id', 'username', 'email', 'xp', 'niveau', 'nom_niveau_display',
            'autocoin_balance', 'progression_pct', 'estimations_ce_mois', 'created_at'
        ]

    def get_nom_niveau_display(self, obj):
        return obj.nom_niveau()

    def get_progression_pct(self, obj):
        return obj.progression_pct()


class TransactionSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'montant', 'type', 'type_display', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class DefiSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Defi
        fields = ['id', 'titre', 'description', 'type', 'type_display', 'xp_reward', 'ac_reward', 'cible_count', 'is_active']


class DefiJoueurSerializer(serializers.ModelSerializer):
    defi_details = DefiSerializer(source='defi', read_only=True)
    pourcentage_progression = serializers.SerializerMethodField()

    class Meta:
        model = DefiJoueur
        fields = ['id', 'defi_details', 'progression', 'pourcentage_progression', 'completed', 'completed_at']

    def get_pourcentage_progression(self, obj):
        if obj.defi.cible_count == 0:
            return 100
        return min(100, int((obj.progression / obj.defi.cible_count) * 100))
