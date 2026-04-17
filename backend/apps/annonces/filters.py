import django_filters
from .models import Annonce

class AnnonceFilter(django_filters.FilterSet):
    marque = django_filters.CharFilter(
        field_name='marque__nom', lookup_expr='iexact'
    )
    modele = django_filters.CharFilter(lookup_expr='icontains')
    annee_min = django_filters.NumberFilter(
        field_name='annee', lookup_expr='gte'
    )
    annee_max = django_filters.NumberFilter(
        field_name='annee', lookup_expr='lte'
    )
    prix_min = django_filters.NumberFilter(
        field_name='prix', lookup_expr='gte'
    )
    prix_max = django_filters.NumberFilter(
        field_name='prix', lookup_expr='lte'
    )
    km_max = django_filters.NumberFilter(
        field_name='kilometrage', lookup_expr='lte'
    )
    carburant = django_filters.CharFilter(lookup_expr='iexact')
    pays = django_filters.CharFilter(lookup_expr='iexact')
    bonne_affaire = django_filters.BooleanFilter(
        field_name='est_bonne_affaire'
    )

    class Meta:
        model = Annonce
        fields = [
            'marque', 'modele', 'annee_min', 'annee_max',
            'prix_min', 'prix_max', 'km_max',
            'carburant', 'pays', 'bonne_affaire'
        ]
