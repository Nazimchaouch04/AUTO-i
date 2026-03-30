from rest_framework import serializers


class DashboardStatsSerializer(serializers.Serializer):
    total_annonces = serializers.IntegerField()
    bonnes_affaires = serializers.IntegerField()
    prix_moyen = serializers.FloatField()
    variation_prix = serializers.FloatField()
