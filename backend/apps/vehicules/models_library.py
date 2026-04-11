from django.db import models
from django.utils.text import slugify
import uuid

class Marque(models.Model):
    """Marques de véhicules avec informations détaillées"""
    nom = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    pays_origine = models.CharField(max_length=100)
    annee_creation = models.IntegerField()
    logo = models.URLField(blank=True)
    description = models.TextField(blank=True)
    site_web = models.URLField(blank=True)
    siege_social = models.CharField(max_length=200, blank=True)
    est_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['nom']
        verbose_name = "Marque"
        verbose_name_plural = "Marques"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nom

class Modele(models.Model):
    """Modèles de véhicules avec spécifications complètes"""
    CATEGORIE_CHOICES = [
        ('berline', 'Berline'),
        ('suv', 'SUV'),
        ('compacte', 'Compacte'),
        ('monospace', 'Monospace'),
        ('coupé', 'Coupé'),
        ('cabriolet', 'Cabriolet'),
        ('break', 'Break'),
        ('pick_up', 'Pick-up'),
        ('utilitaire', 'Utilitaire'),
        ('sportive', 'Sportive'),
        ('hybride', 'Hybride'),
        ('electrique', 'Électrique'),
    ]
    
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name='modeles')
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    annee_lancement = models.IntegerField()
    annee_arret = models.IntegerField(null=True, blank=True)
    generation = models.CharField(max_length=50, blank=True)
    code_chassis = models.CharField(max_length=50, blank=True)
    
    # Dimensions
    longueur = models.FloatField(null=True, blank=True)  # en mm
    largeur = models.FloatField(null=True, blank=True)   # en mm
    hauteur = models.FloatField(null=True, blank=True)   # en mm
    empattement = models.FloatField(null=True, blank=True)  # en mm
    poids_vide = models.FloatField(null=True, blank=True)     # en kg
    volume_coffre = models.FloatField(null=True, blank=True)   # en litres
    
    # Moteur et performances
    type_moteur = models.CharField(max_length=50, blank=True)
    cylindree = models.FloatField(null=True, blank=True)  # en cm3
    puissance_max = models.FloatField(null=True, blank=True)  # en ch
    couple_max = models.FloatField(null=True, blank=True)      # en Nm
    vitesse_max = models.FloatField(null=True, blank=True)       # en km/h
    acceleration_0_100 = models.FloatField(null=True, blank=True)  # en secondes
    
    # Consommation et émissions
    consommation_mixte = models.FloatField(null=True, blank=True)  # L/100km
    consommation_urbaine = models.FloatField(null=True, blank=True)  # L/100km
    consommation_extra_urbaine = models.FloatField(null=True, blank=True)  # L/100km
    emissions_co2 = models.FloatField(null=True, blank=True)  # g/km
    
    # Transmission
    type_boite = models.CharField(max_length=50, blank=True)
    nombre_vitesses = models.IntegerField(null=True, blank=True)
    transmission = models.CharField(max_length=20, choices=[
        ('traction', 'Traction'),
        ('propulsion', 'Propulsion'),
        ('4x4', '4x4'),
        ('integrale', 'Transmission intégrale'),
    ], blank=True)
    
    # Freinage et sécurité
    systeme_freinage = models.CharField(max_length=100, blank=True)
    nombre_airbags = models.IntegerField(null=True, blank=True)
    note_euro_ncap = models.IntegerField(null=True, blank=True)
    annee_test_ncap = models.IntegerField(null=True, blank=True)
    
    # Équipements
    nombre_portes = models.IntegerField(null=True, blank=True)
    nombre_places = models.IntegerField(null=True, blank=True)
    climatisation = models.BooleanField(default=False)
    gps = models.BooleanField(default=False)
    bluetooth = models.BooleanField(default=False)
    usb = models.BooleanField(default=False)
    camera_recul = models.BooleanField(default=False)
    capteurs_stationnement = models.BooleanField(default=False)
    regulateur_vitesse = models.BooleanField(default=False)
    limiteur_vitesse = models.BooleanField(default=False)
    aide_freinage_urgence = models.BooleanField(default=False)
    detection_angle_mort = models.BooleanField(default=False)
    alerte_franchissement_ligne = models.BooleanField(default=False)
    
    # Prix et marché
    prix_neuf_lancement = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix_neuf_actuel = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix_occasion_moyen = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cout_entretien_annuel = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    taxe_mise_en_circulation = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Fiabilité et entretien
    indice_fiabilite = models.IntegerField(null=True, blank=True)  # 1-100
    frequence_entretien = models.IntegerField(null=True, blank=True)  # en km
    duree_garantie = models.IntegerField(null=True, blank=True)  # en mois/km
    pieces_detachees_disponibles = models.BooleanField(default=True)
    
    # Informations supplémentaires
    description = models.TextField(blank=True)
    points_forts = models.TextField(blank=True)
    points_faibles = models.TextField(blank=True)
    concurrents = models.TextField(blank=True)
    image_principale = models.URLField(blank=True)
    images_supplementaires = models.JSONField(default=list, blank=True)
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    est_actif = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['marque', 'nom']
        unique_together = ['marque', 'nom']
        verbose_name = "Modèle"
        verbose_name_plural = "Modèles"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.marque.nom} {self.nom}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.marque.nom} {self.nom}"
    
    @property
    def nom_complet(self):
        return f"{self.marque.nom} {self.nom}"
    
    @property
    def prix_formate_neuf(self):
        if self.prix_neuf_actuel:
            return f"{int(self.prix_neuf_actuel):,}€".replace(',', ' ')
        return "N/A"
    
    @property
    def prix_formate_occasion(self):
        if self.prix_occasion_moyen:
            return f"{int(self.prix_occasion_moyen):,}€".replace(',', ' ')
        return "N/A"

class Motorisation(models.Model):
    """Motorisations disponibles pour chaque modèle"""
    CARBURANT_CHOICES = [
        ('essence', 'Essence'),
        ('diesel', 'Diesel'),
        ('hybride', 'Hybride'),
        ('electrique', 'Électrique'),
        ('gpl', 'GPL'),
        ('ethanol', 'Éthanol'),
        ('hybride_rechargeable', 'Hybride rechargeable'),
    ]
    
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE, related_name='motorisations')
    nom_commercial = models.CharField(max_length=100)
    type_carburant = models.CharField(max_length=25, choices=CARBURANT_CHOICES)
    cylindree = models.FloatField(null=True, blank=True)
    puissance = models.FloatField(null=True, blank=True)  # en ch
    couple = models.FloatField(null=True, blank=True)    # en Nm
    
    # Performances
    vitesse_max = models.FloatField(null=True, blank=True)
    acceleration_0_100 = models.FloatField(null=True, blank=True)
    
    # Consommation
    consommation_mixte = models.FloatField(null=True, blank=True)
    consommation_urbaine = models.FloatField(null=True, blank=True)
    consommation_extra_urbaine = models.FloatField(null=True, blank=True)
    emissions_co2 = models.FloatField(null=True, blank=True)
    
    # Électrique/Hybride
    autonomie_electrique = models.FloatField(null=True, blank=True)  # en km
    capacite_batterie = models.FloatField(null=True, blank=True)     # en kWh
    temps_recharge = models.FloatField(null=True, blank=True)        # en heures
    
    # Prix
    prix_neuf = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    malus_ecologique = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    bonus_ecologique = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Disponibilité
    date_lancement = models.DateField(null=True, blank=True)
    date_arret = models.DateField(null=True, blank=True)
    est_disponible = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['modele', 'nom_commercial']
        verbose_name = "Motorisation"
        verbose_name_plural = "Motorisations"
    
    def __str__(self):
        return f"{self.modele.nom_complet} - {self.nom_commercial}"

class Finition(models.Model):
    """Finitions disponibles pour chaque modèle"""
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE, related_name='finitions')
    nom = models.CharField(max_length=100)
    niveau = models.IntegerField(help_text="1=Basique, 5=Luxe")
    description = models.TextField(blank=True)
    
    # Équipements de série
    equipements_serie = models.JSONField(default=list, blank=True)
    
    # Options disponibles
    options_disponibles = models.JSONField(default=list, blank=True)
    
    # Prix
    prix_neuf = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix_options_moyen = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Popularité
    est_plus_vendue = models.BooleanField(default=False)
    pourcentage_ventes = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['modele', 'niveau', 'nom']
        verbose_name = "Finition"
        verbose_name_plural = "Finitions"
    
    def __str__(self):
        return f"{self.modele.nom_complet} - {self.nom}"

class Equipement(models.Model):
    """Catalogue d'équipements automobiles"""
    CATEGORIE_CHOICES = [
        ('securite', 'Sécurité'),
        ('confort', 'Confort'),
        ('multimedia', 'Multimédia'),
        ('performance', 'Performance'),
        ('exterieur', 'Extérieur'),
        ('interieur', 'Intérieur'),
        ('aide_conduite', 'Aide à la conduite'),
        ('ecologie', 'Écologie'),
    ]
    
    nom = models.CharField(max_length=100)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    description = models.TextField(blank=True)
    technologie = models.CharField(max_length=100, blank=True)
    
    # Coût et valeur
    prix_moyen_option = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    valeur_revente = models.IntegerField(null=True, blank=True)  # 1-100
    
    # Disponibilité par marque
    marques_disponibles = models.ManyToManyField(Marque, blank=True)
    
    class Meta:
        ordering = ['categorie', 'nom']
        verbose_name = "Équipement"
        verbose_name_plural = "Équipements"
    
    def __str__(self):
        return f"{self.categorie.title()} - {self.nom}"

class AvisExpert(models.Model):
    """Avis d'experts sur les modèles"""
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE, related_name='avis_experts')
    source = models.CharField(max_length=100)  # Nom du média/expert
    auteur = models.CharField(max_length=100)
    note_globale = models.FloatField(help_text="Note sur 10")
    
    # Notes détaillées
    note_conduite = models.FloatField(null=True, blank=True)
    note_confort = models.FloatField(null=True, blank=True)
    note_habitabilite = models.FloatField(null=True, blank=True)
    note_equipements = models.FloatField(null=True, blank=True)
    note_fiabilite = models.FloatField(null=True, blank=True)
    note_rapport_qualite_prix = models.FloatField(null=True, blank=True)
    
    # Contenu
    titre_avis = models.CharField(max_length=200)
    contenu = models.TextField()
    points_forts = models.TextField(blank=True)
    points_faibles = models.TextField(blank=True)
    
    # Métadonnées
    date_publication = models.DateField()
    url_source = models.URLField(blank=True)
    est_verifie = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_publication']
        verbose_name = "Avis d'expert"
        verbose_name_plural = "Avis d'experts"
    
    def __str__(self):
        return f"{self.modele.nom_complet} - {self.source} ({self.note_globale}/10)"

class ProblemeCourant(models.Model):
    """Problèmes courants par modèle"""
    GRAVITE_CHOICES = [
        (1, 'Mineur'),
        (2, 'Modéré'),
        (3, 'Majeur'),
        (4, 'Critique'),
    ]
    
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE, related_name='problemes_courants')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    
    # Informations sur le problème
    gravite = models.IntegerField(choices=GRAVITE_CHOICES)
    frequence_apparition = models.IntegerField(help_text="Pourcentage de véhicules affectés")
    kilometrage_moyen_apparition = models.IntegerField(null=True, blank=True, help_text="En km")
    annees_concernees = models.CharField(max_length=50, blank=True, help_text="Ex: 2015-2018")
    
    # Réparation
    cout_reparation_moyen = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    temps_reparation = models.FloatField(null=True, blank=True, help_text="En heures")
    pieces_changees = models.TextField(blank=True)
    
    # Recalls et garanties
    est_couvert_garantie = models.BooleanField(default=False)
    campagne_rappel = models.BooleanField(default=False)
    reference_rappel = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-gravite', '-frequence_apparition']
        verbose_name = "Problème courant"
        verbose_name_plural = "Problèmes courants"
    
    def __str__(self):
        return f"{self.modele.nom_complet} - {self.titre}"

class DonneeMarche(models.Model):
    """Données de marché par modèle"""
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE, related_name='donnees_marche')
    pays = models.CharField(max_length=5, default='DZ')
    annee = models.IntegerField()
    
    # Ventes
    ventes_annuelles = models.IntegerField(default=0)
    ventes_cumulees = models.IntegerField(default=0)
    part_marche = models.FloatField(default=0, help_text="En pourcentage")
    
    # Prix du marché
    prix_neuf_moyen = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix_occasion_moyen = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    depreciation_3_ans = models.FloatField(null=True, blank=True, help_text="En pourcentage")
    
    # Popularité
    classement_categorie = models.IntegerField(null=True, blank=True)
    temps_vente_moyen = models.FloatField(null=True, blank=True, help_text="En jours")
    
    class Meta:
        ordering = ['-annee', '-ventes_annuelles']
        unique_together = ['modele', 'pays', 'annee']
        verbose_name = "Donnée de marché"
        verbose_name_plural = "Données de marché"
    
    def __str__(self):
        return f"{self.modele.nom_complet} - {self.pays} {self.annee}"
