from rest_framework import serializers
from .models_library import (
    Marque, Modele, Motorisation, Finition, Equipement,
    AvisExpert, ProblemeCourant, DonneeMarche
)


class MarqueSerializer(serializers.ModelSerializer):
    nombre_modeles = serializers.SerializerMethodField()
    
    class Meta:
        model = Marque
        fields = [
            'id', 'nom', 'slug', 'pays_origine', 'annee_creation', 'logo',
            'description', 'site_web', 'siege_social', 'est_active', 'nombre_modeles'
        ]
        read_only_fields = ['slug']
    
    def get_nombre_modeles(self, obj):
        return obj.modeles.filter(est_actif=True).count()


class MotorisationSerializer(serializers.ModelSerializer):
    type_carburant_display = serializers.CharField(source='get_type_carburant_display', read_only=True)
    prix_formate = serializers.SerializerMethodField()
    
    class Meta:
        model = Motorisation
        fields = [
            'id', 'modele', 'nom_commercial', 'type_carburant', 'type_carburant_display',
            'cylindree', 'puissance', 'couple', 'vitesse_max', 'acceleration_0_100',
            'consommation_mixte', 'consommation_urbaine', 'consommation_extra_urbaine',
            'emissions_co2', 'autonomie_electrique', 'capacite_batterie', 'temps_recharge',
            'prix_neuf', 'malus_ecologique', 'bonus_ecologique', 'date_lancement',
            'date_arret', 'est_disponible', 'prix_formate'
        ]
    
    def get_prix_formate(self, obj):
        if obj.prix_neuf:
            return f"{int(obj.prix_neuf):,}€".replace(',', ' ')
        return "N/A"


class FinitionSerializer(serializers.ModelSerializer):
    prix_formate = serializers.SerializerMethodField()
    prix_options_formate = serializers.SerializerMethodField()
    
    class Meta:
        model = Finition
        fields = [
            'id', 'modele', 'nom', 'niveau', 'description', 'equipements_serie',
            'options_disponibles', 'prix_neuf', 'prix_options_moyen',
            'prix_formate', 'prix_options_formate', 'est_plus_vendue', 'pourcentage_ventes'
        ]
    
    def get_prix_formate(self, obj):
        if obj.prix_neuf:
            return f"{int(obj.prix_neuf):,}€".replace(',', ' ')
        return "N/A"
    
    def get_prix_options_formate(self, obj):
        if obj.prix_options_moyen:
            return f"{int(obj.prix_options_moyen):,}€".replace(',', ' ')
        return "N/A"


class EquipementSerializer(serializers.ModelSerializer):
    categorie_display = serializers.CharField(source='get_categorie_display', read_only=True)
    prix_formate = serializers.SerializerMethodField()
    
    class Meta:
        model = Equipement
        fields = [
            'id', 'nom', 'categorie', 'categorie_display', 'description', 'technologie',
            'prix_moyen_option', 'prix_formate', 'valeur_revente', 'marques_disponibles'
        ]
    
    def get_prix_formate(self, obj):
        if obj.prix_moyen_option:
            return f"{int(obj.prix_moyen_option):,}€".replace(',', ' ')
        return "N/A"


class AvisExpertSerializer(serializers.ModelSerializer):
    modele_nom = serializers.CharField(source='modele.nom_complet', read_only=True)
    modele_marque = serializers.CharField(source='modele.marque.nom', read_only=True)
    
    class Meta:
        model = AvisExpert
        fields = [
            'id', 'modele', 'modele_nom', 'modele_marque', 'source', 'auteur',
            'note_globale', 'note_conduite', 'note_confort', 'note_habitabilite',
            'note_equipements', 'note_fiabilite', 'note_rapport_qualite_prix',
            'titre_avis', 'contenu', 'points_forts', 'points_faibles',
            'date_publication', 'url_source', 'est_verifie'
        ]
        read_only_fields = ['date_publication']


class ProblemeCourantSerializer(serializers.ModelSerializer):
    modele_nom = serializers.CharField(source='modele.nom_complet', read_only=True)
    gravite_display = serializers.CharField(source='get_gravite_display', read_only=True)
    cout_formate = serializers.SerializerMethodField()
    
    class Meta:
        model = ProblemeCourant
        fields = [
            'id', 'modele', 'modele_nom', 'titre', 'description', 'gravite',
            'gravite_display', 'frequence_apparition', 'kilometrage_moyen_apparition',
            'annees_concernees', 'cout_reparation_moyen', 'cout_formate',
            'temps_reparation', 'pieces_changees', 'est_couvert_garantie',
            'campagne_rappel', 'reference_rappel'
        ]
    
    def get_cout_formate(self, obj):
        if obj.cout_reparation_moyen:
            return f"{int(obj.cout_reparation_moyen):,}€".replace(',', ' ')
        return "N/A"


class DonneeMarcheSerializer(serializers.ModelSerializer):
    modele_nom = serializers.CharField(source='modele.nom_complet', read_only=True)
    prix_neuf_formate = serializers.SerializerMethodField()
    prix_occasion_formate = serializers.SerializerMethodField()
    
    class Meta:
        model = DonneeMarche
        fields = [
            'id', 'modele', 'modele_nom', 'pays', 'annee', 'ventes_annuelles',
            'ventes_cumulees', 'part_marche', 'prix_neuf_moyen', 'prix_occasion_moyen',
            'prix_neuf_formate', 'prix_occasion_formate', 'depreciation_3_ans',
            'classement_categorie', 'temps_vente_moyen'
        ]
    
    def get_prix_neuf_formate(self, obj):
        if obj.prix_neuf_moyen:
            return f"{int(obj.prix_neuf_moyen):,}€".replace(',', ' ')
        return "N/A"
    
    def get_prix_occasion_formate(self, obj):
        if obj.prix_occasion_moyen:
            return f"{int(obj.prix_occasion_moyen):,}€".replace(',', ' ')
        return "N/A"


class ModeleSerializer(serializers.ModelSerializer):
    marque_nom = serializers.CharField(source='marque.nom', read_only=True)
    categorie_display = serializers.CharField(source='get_categorie_display', read_only=True)
    transmission_display = serializers.CharField(source='get_transmission_display', read_only=True)
    
    # Prix formatés
    prix_neuf_formate = serializers.SerializerMethodField()
    prix_occasion_formate = serializers.SerializerMethodField()
    cout_entretien_formate = serializers.SerializerMethodField()
    
    # Données calculées
    nombre_motorisations = serializers.SerializerMethodField()
    nombre_finitions = serializers.SerializerMethodField()
    nombre_avis = serializers.SerializerMethodField()
    nombre_problemes = serializers.SerializerMethodField()
    
    # Équipements principaux
    equipements_principaux = serializers.SerializerMethodField()
    
    class Meta:
        model = Modele
        fields = [
            'id', 'marque', 'marque_nom', 'nom', 'slug', 'categorie', 'categorie_display',
            'annee_lancement', 'annee_arret', 'generation', 'code_chassis',
            
            # Dimensions
            'longueur', 'largeur', 'hauteur', 'empattement', 'poids_vide', 'volume_coffre',
            
            # Moteur et performances
            'type_moteur', 'cylindree', 'puissance_max', 'couple_max', 'vitesse_max',
            'acceleration_0_100',
            
            # Consommation et émissions
            'consommation_mixte', 'consommation_urbaine', 'consommation_extra_urbaine',
            'emissions_co2',
            
            # Transmission
            'type_boite', 'nombre_vitesses', 'transmission', 'transmission_display',
            
            # Sécurité
            'systeme_freinage', 'nombre_airbags', 'note_euro_ncap', 'annee_test_ncap',
            
            # Équipements
            'nombre_portes', 'nombre_places', 'climatisation', 'gps', 'bluetooth',
            'usb', 'camera_recul', 'capteurs_stationnement', 'regulateur_vitesse',
            'limiteur_vitesse', 'aide_freinage_urgence', 'detection_angle_mort',
            'alerte_franchissement_ligne',
            
            # Prix et marché
            'prix_neuf_lancement', 'prix_neuf_actuel', 'prix_occasion_moyen',
            'cout_entretien_annuel', 'taxe_mise_en_circulation',
            'prix_neuf_formate', 'prix_occasion_formate', 'cout_entretien_formate',
            
            # Fiabilité
            'indice_fiabilite', 'frequence_entretien', 'duree_garantie',
            'pieces_detachees_disponibles',
            
            # Informations
            'description', 'points_forts', 'points_faibles', 'concurrents',
            'image_principale', 'images_supplementaires',
            
            # Métadonnées
            'date_creation', 'date_mise_a_jour', 'est_actif',
            
            # Données calculées
            'nombre_motorisations', 'nombre_finitions', 'nombre_avis', 'nombre_problemes',
            'equipements_principaux'
        ]
        read_only_fields = ['slug', 'date_creation', 'date_mise_a_jour']
    
    def get_prix_neuf_formate(self, obj):
        if obj.prix_neuf_actuel:
            return f"{int(obj.prix_neuf_actuel):,}€".replace(',', ' ')
        return "N/A"
    
    def get_prix_occasion_formate(self, obj):
        if obj.prix_occasion_moyen:
            return f"{int(obj.prix_occasion_moyen):,}€".replace(',', ' ')
        return "N/A"
    
    def get_cout_entretien_formate(self, obj):
        if obj.cout_entretien_annuel:
            return f"{int(obj.cout_entretien_annuel):,}€".replace(',', ' ')
        return "N/A"
    
    def get_nombre_motorisations(self, obj):
        return obj.motorisations.filter(est_disponible=True).count()
    
    def get_nombre_finitions(self, obj):
        return obj.finitions.count()
    
    def get_nombre_avis(self, obj):
        return obj.avis_experts.count()
    
    def get_nombre_problemes(self, obj):
        return obj.problemes_courants.count()
    
    def get_equipements_principaux(self, obj):
        equipements = []
        
        if obj.climatisation:
            equipements.append('Climatisation')
        if obj.gps:
            equipements.append('GPS')
        if obj.bluetooth:
            equipements.append('Bluetooth')
        if obj.camera_recul:
            equipements.append('Caméra de recul')
        if obj.capteurs_stationnement:
            equipements.append('Capteurs de stationnement')
        if obj.aide_freinage_urgence:
            equipements.append('Aide au freinage d\'urgence')
        if obj.detection_angle_mort:
            equipements.append('Détection d\'angle mort')
        
        return equipements


class ModeleDetailSerializer(ModeleSerializer):
    """Sérialiseur détaillé pour un modèle complet"""
    motorisations = MotorisationSerializer(many=True, read_only=True)
    finitions = FinitionSerializer(many=True, read_only=True)
    avis_experts = AvisExpertSerializer(many=True, read_only=True)
    problemes_courants = ProblemeCourantSerializer(many=True, read_only=True)
    donnees_marche = DonneeMarcheSerializer(many=True, read_only=True)
    
    class Meta(ModeleSerializer.Meta):
        fields = ModeleSerializer.Meta.fields + [
            'motorisations', 'finitions', 'avis_experts', 'problemes_courants', 'donnees_marche'
        ]


class ComparaisonModeleSerializer(serializers.Serializer):
    """Sérialiseur pour la comparaison de modèles"""
    modele_principal = ModeleSerializer()
    concurrents = ModeleSerializer(many=True)
    criteres_comparaison = serializers.ListField(child=serializers.CharField())
    
    def validate_criteres_comparaison(self, value):
        criteres_valides = [
            'prix_occasion_moyen', 'consommation_mixte', 'acceleration_0_100',
            'note_euro_ncap', 'indice_fiabilite', 'volume_coffre',
            'nombre_places', 'puissance_max', 'emissions_co2'
        ]
        
        for critere in value:
            if critere not in criteres_valides:
                raise serializers.ValidationError(f"Critère de comparaison invalide: {critere}")
        
        return value


class RechercheAvanceeSerializer(serializers.Serializer):
    """Sérialiseur pour la recherche avancée"""
    recherche = serializers.CharField(required=False)
    categories = serializers.ListField(child=serializers.CharField(), required=False)
    marques = serializers.ListField(child=serializers.CharField(), required=False)
    prix_min = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    prix_max = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    annee_min = serializers.IntegerField(required=False)
    annee_max = serializers.IntegerField(required=False)
    tri = serializers.ChoiceField(
        choices=['prix_asc', 'prix_desc', 'fiabilite', 'consommation', 'annee'],
        default='prix_occasion_moyen'
    )
    page = serializers.IntegerField(default=1)
    page_size = serializers.IntegerField(default=20)


class StatistiquesGlobalesSerializer(serializers.Serializer):
    """Sérialiseur pour les statistiques globales"""
    stats_generales = serializers.DictField()
    repartition_categories = serializers.ListField()
    top_marques = serializers.ListField()
    prix_par_categorie = serializers.ListField()


class SuggestionRechercheSerializer(serializers.Serializer):
    """Sérialiseur pour les suggestions de recherche"""
    marques = serializers.ListField(child=serializers.CharField())
    modeles = serializers.ListField(child=serializers.DictField())
