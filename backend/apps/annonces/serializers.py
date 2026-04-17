from rest_framework import serializers
from .models import Annonce, Marque

class MarqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marque
        fields = ['id', 'nom', 'slug', 'populaire']

class AnnonceListSerializer(serializers.ModelSerializer):
    marque_nom = serializers.CharField(source='marque.nom', read_only=True)
    
    class Meta:
        model = Annonce
        fields = [
            'id', 'marque_nom', 'modele', 'annee', 'kilometrage',
            'carburant', 'boite', 'prix', 'prix_estime',
            'ecart_prix', 'est_bonne_affaire', 'score_affaire',
            'ville', 'pays', 'date_publication',
        ]

class AnnonceDetailSerializer(AnnonceListSerializer):
    class Meta(AnnonceListSerializer.Meta):
        fields = AnnonceListSerializer.Meta.fields + [
            'puissance', 'description', 'url_originale', 'source',
            'created_at',
        ]
