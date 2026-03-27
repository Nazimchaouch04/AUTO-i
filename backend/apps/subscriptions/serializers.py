from rest_framework import serializers
from .models import Plan, Abonnement


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'nom', 'prix_mensuel', 'estimations_par_mois',
                  'alertes_max', 'export_csv', 'acces_api']


class AbonnementSerializer(serializers.ModelSerializer):
    plan_nom = serializers.CharField(source='plan.nom', read_only=True)
    plan_details = PlanSerializer(source='plan', read_only=True)

    class Meta:
        model = Abonnement
        fields = ['id', 'plan_nom', 'plan_details', 'actif', 'date_debut', 'date_fin']
