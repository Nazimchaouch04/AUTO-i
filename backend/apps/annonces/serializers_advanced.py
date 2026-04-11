from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Annonce, Favori, RechercheSauvegardee
from .models_advanced import (
    Signalement, ContactVendeur, EvaluationVendeur, 
    NotificationAnnonce, ComparaisonAnnonce, AlerteRecherche,
    HistoriqueRecherche, VisiteAnnonce
)


class FavoriSerializer(serializers.ModelSerializer):
    annonce_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Favori
        fields = ['id', 'annonce', 'annonce_details', 'created_at']
        read_only_fields = ['created_at']
    
    def get_annonce_details(self, obj):
        annonce = obj.annonce
        return {
            'id': str(annonce.id),
            'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele}",
            'marque': annonce.vehicule.marque,
            'modele': annonce.vehicule.modele,
            'annee': annonce.annee,
            'kilometrage': annonce.kilometrage,
            'prix': annonce.prix,
            'prix_formate': f"{int(annonce.prix):,}€".replace(',', ' '),
            'ville': annonce.ville,
            'pays': annonce.pays,
            'images': annonce.images,
            'est_bonne_affaire': annonce.est_bonne_affaire,
            'score_affaire': annonce.score_affaire,
            'date_publication': annonce.date_publication,
        }


class RechercheSauvegardeeSerializer(serializers.ModelSerializer):
    nombre_resultats_formate = serializers.SerializerMethodField()
    
    class Meta:
        model = RechercheSauvegardee
        fields = ['id', 'nom', 'query_params', 'result_count', 'nombre_resultats_formate', 'created_at']
        read_only_fields = ['created_at', 'result_count']
    
    def get_nombre_resultats_formate(self, obj):
        return f"{obj.result_count:,} résultat{'s' if obj.result_count > 1 else ''}".replace(',', ' ')


class SignalementSerializer(serializers.ModelSerializer):
    annonce_details = serializers.SerializerMethodField()
    utilisateur_nom = serializers.CharField(source='utilisateur.username', read_only=True)
    
    class Meta:
        model = Signalement
        fields = [
            'id', 'annonce', 'annonce_details', 'utilisateur', 'utilisateur_nom',
            'raison', 'description', 'date_signalement', 'est_traite',
            'traite_par', 'date_traitement', 'note_traitement'
        ]
        read_only_fields = ['date_signalement', 'utilisateur']
    
    def get_annonce_details(self, obj):
        annonce = obj.annonce
        return {
            'id': str(annonce.id),
            'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele}",
            'prix': annonce.prix,
            'ville': annonce.ville,
        }


class ContactVendeurSerializer(serializers.ModelSerializer):
    acheteur_nom = serializers.CharField(source='acheteur_potentiel.username', read_only=True)
    annonce_details = serializers.SerializerMethodField()
    
    class Meta:
        model = ContactVendeur
        fields = [
            'id', 'annonce', 'annonce_details', 'acheteur_potentiel', 'acheteur_nom',
            'message', 'telephone_contact', 'email_contact', 'date_contact', 'est_repondu'
        ]
        read_only_fields = ['date_contact', 'acheteur_potentiel', 'email_contact']
    
    def get_annonce_details(self, obj):
        annonce = obj.annonce
        return {
            'id': str(annonce.id),
            'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele}",
            'prix': annonce.prix,
            'vendeur': annonce.vendeur.username if annonce.vendeur else 'Anonyme',
        }


class EvaluationVendeurSerializer(serializers.ModelSerializer):
    evaluateur_nom = serializers.CharField(source='evaluateur.username', read_only=True)
    vendeur_nom = serializers.CharField(source='vendeur.username', read_only=True)
    annonce_details = serializers.SerializerMethodField()
    
    class Meta:
        model = EvaluationVendeur
        fields = [
            'id', 'vendeur', 'vendeur_nom', 'evaluateur', 'evaluateur_nom',
            'annonce', 'annonce_details', 'note', 'commentaire', 'aspects',
            'date_evaluation'
        ]
        read_only_fields = ['date_evaluation', 'evaluateur']
    
    def get_annonce_details(self, obj):
        annonce = obj.annonce
        return {
            'id': str(annonce.id),
            'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele}",
        }
    
    def validate_note(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La note doit être comprise entre 1 et 5.")
        return value


class NotificationAnnonceSerializer(serializers.ModelSerializer):
    annonce_details = serializers.SerializerMethodField()
    est_lue_formate = serializers.SerializerMethodField()
    
    class Meta:
        model = NotificationAnnonce
        fields = [
            'id', 'utilisateur', 'type_notification', 'annonce', 'annonce_details',
            'titre', 'message', 'date_creation', 'est_lue', 'est_lue_formate',
            'date_lecture', 'donnees_supplementaires'
        ]
        read_only_fields = ['date_creation', 'utilisateur']
    
    def get_annonce_details(self, obj):
        if obj.annonce:
            return {
                'id': str(obj.annonce.id),
                'titre': f"{obj.annonce.vehicule.marque} {obj.annonce.vehicule.modele}",
                'prix': obj.annonce.prix,
            }
        return None
    
    def get_est_lue_formate(self, obj):
        if obj.est_lue:
            return f"Lue le {obj.date_lecture.strftime('%d/%m/%Y à %H:%M')}" if obj.date_lecture else "Lue"
        return "Non lue"


class ComparaisonAnnonceSerializer(serializers.ModelSerializer):
    annonces_details = serializers.SerializerMethodField()
    nombre_annonces = serializers.SerializerMethodField()
    
    class Meta:
        model = ComparaisonAnnonce
        fields = [
            'id', 'user', 'nom', 'annonces', 'annonces_details', 'nombre_annonces',
            'criteres', 'date_creation', 'est_publique', 'slug'
        ]
        read_only_fields = ['date_creation', 'user', 'slug']
    
    def get_nombre_annonces(self, obj):
        return obj.annonces.count()
    
    def get_annonces_details(self, obj):
        annonces = obj.annonces.all()
        return [
            {
                'id': str(annonce.id),
                'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele}",
                'marque': annonce.vehicule.marque,
                'modele': annonce.vehicule.modele,
                'annee': annonce.annee,
                'kilometrage': annonce.kilometrage,
                'prix': annonce.prix,
                'prix_formate': f"{int(annonce.prix):,}€".replace(',', ' '),
                'ville': annonce.ville,
                'pays': annonce.pays,
                'images': annonce.images,
                'est_bonne_affaire': annonce.est_bonne_affaire,
                'score_affaire': annonce.score_affaire,
            }
            for annonce in annonces
        ]


class AlerteRechercheSerializer(serializers.ModelSerializer):
    nombre_resultats_formate = serializers.SerializerMethodField()
    derniere_notification_formate = serializers.SerializerMethodField()
    
    class Meta:
        model = AlerteRecherche
        fields = [
            'id', 'user', 'nom', 'filtres', 'frequence', 'est_active',
            'date_creation', 'derniere_notification', 'derniere_notification_formate',
            'nombre_resultats', 'nombre_resultats_formate'
        ]
        read_only_fields = ['date_creation', 'user', 'derniere_notification', 'nombre_resultats']
    
    def get_nombre_resultats_formate(self, obj):
        return f"{obj.nombre_resultats:,} résultat{'s' if obj.nombre_resultats > 1 else ''}".replace(',', ' ')
    
    def get_derniere_notification_formate(self, obj):
        if obj.derniere_notification:
            return obj.derniere_notification.strftime('%d/%m/%Y à %H:%M')
        return "Jamais"


class HistoriqueRechercheSerializer(serializers.ModelSerializer):
    nombre_resultats_formate = serializers.SerializerMethodField()
    filtres_formates = serializers.SerializerMethodField()
    
    class Meta:
        model = HistoriqueRecherche
        fields = [
            'id', 'user', 'terme', 'filtres', 'filtres_formates',
            'nombre_resultats', 'nombre_resultats_formate', 'date_recherche'
        ]
        read_only_fields = ['date_recherche', 'user', 'nombre_resultats']
    
    def get_nombre_resultats_formate(self, obj):
        return f"{obj.nombre_resultats:,} résultat{'s' if obj.nombre_resultats > 1 else ''}".replace(',', ' ')
    
    def get_filtres_formates(self, obj):
        filtres = obj.filtres
        formates = []
        
        if filtres.get('marque'):
            formates.append(f"Marque: {filtres['marque']}")
        if filtres.get('prix_min'):
            formates.append(f"Prix min: {int(filtres['prix_min']):,}€".replace(',', ' '))
        if filtres.get('prix_max'):
            formates.append(f"Prix max: {int(filtres['prix_max']):,}€".replace(',', ' '))
        if filtres.get('km_max'):
            formates.append(f"KM max: {filtres['km_max']:,} km".replace(',', ' '))
        if filtres.get('annee_min'):
            formates.append(f"Année min: {filtres['annee_min']}")
        if filtres.get('carburant'):
            formates.append(f"Carburant: {filtres['carburant']}")
        
        return formates


class VisiteAnnonceSerializer(serializers.ModelSerializer):
    annonce_details = serializers.SerializerMethodField()
    utilisateur_nom = serializers.CharField(source='utilisateur.username', read_only=True)
    duree_visite_formate = serializers.SerializerMethodField()
    
    class Meta:
        model = VisiteAnnonce
        fields = [
            'id', 'annonce', 'annonce_details', 'utilisateur', 'utilisateur_nom',
            'ip_address', 'user_agent', 'date_visite', 'duree_visite',
            'duree_visite_formate', 'provient_de'
        ]
        read_only_fields = ['date_visite', 'ip_address', 'user_agent']
    
    def get_annonce_details(self, obj):
        annonce = obj.annonce
        return {
            'id': str(annonce.id),
            'titre': f"{annonce.vehicule.marque} {annonce.vehicule.modele}",
            'prix': annonce.prix,
        }
    
    def get_duree_visite_formate(self, obj):
        if obj.duree_visite:
            if obj.duree_visite < 60:
                return f"{obj.duree_visite}s"
            elif obj.duree_visite < 3600:
                minutes = obj.duree_visite // 60
                secondes = obj.duree_visite % 60
                return f"{minutes}m {secondes}s"
            else:
                heures = obj.duree_visite // 3600
                minutes = (obj.duree_visite % 3600) // 60
                return f"{heures}h {minutes}m"
        return "N/A"


class AnnonceDetailSerializer(serializers.ModelSerializer):
    """Sérialiseur détaillé pour une annonce complète"""
    vehicule_details = serializers.SerializerMethodField()
    prix_formate = serializers.SerializerMethodField()
    kilometrage_formate = serializers.SerializerMethodField()
    est_favori = serializers.SerializerMethodField()
    nombre_vues = serializers.SerializerMethodField()
    nombre_contacts = serializers.SerializerMethodField()
    evaluation_vendeur = serializers.SerializerMethodField()
    
    class Meta:
        model = Annonce
        fields = [
            'id', 'titre', 'description', 'vehicule', 'vehicule_details',
            'prix', 'prix_formate', 'prix_negociable', 'prix_estime',
            'ecart_prix', 'score_affaire', 'est_bonne_affaire',
            'annee', 'kilometrage', 'kilometrage_formate', 'couleur',
            'transmission', 'carburant', 'puissance', 'cylindree',
            'portes', 'places', 'etat', 'categorie', 'premier_main',
            'ville', 'pays', 'code_postal', 'images', 'video_url',
            'vendeur', 'est_professionnel', 'nom_vendeur', 'telephone',
            'email', 'est_active', 'est_verifiee', 'est_mise_en_avant',
            'date_publication', 'date_mise_a_jour', 'date_expiration',
            'vues', 'contacts', 'sauvegardes',
            'est_favori', 'nombre_vues', 'nombre_contacts',
            'evaluation_vendeur'
        ]
    
    def get_vehicule_details(self, obj):
        return {
            'marque': obj.vehicule.marque,
            'modele': obj.vehicule.modele,
            'categorie': obj.vehicule.categorie,
        }
    
    def get_prix_formate(self, obj):
        return f"{int(obj.prix):,}€".replace(',', ' ')
    
    def get_kilometrage_formate(self, obj):
        return f"{obj.kilometrage:,} km".replace(',', ' ')
    
    def get_est_favori(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favori.objects.filter(
                user=request.user, 
                annonce=obj
            ).exists()
        return False
    
    def get_nombre_vues(self, obj):
        return obj.vues
    
    def get_nombre_contacts(self, obj):
        return obj.contacts
    
    def get_evaluation_vendeur(self, obj):
        if obj.vendeur:
            evaluations = EvaluationVendeur.objects.filter(vendeur=obj.vendeur)
            if evaluations.exists():
                avg_note = evaluations.aggregate(avg_note=serializers.Avg('note'))['avg_note']
                return {
                    'note_moyenne': round(avg_note, 1),
                    'nombre_evaluations': evaluations.count(),
                }
        return None


class UserStatsSerializer(serializers.Serializer):
    """Sérialiseur pour les statistiques utilisateur"""
    stats_generales = serializers.DictField()
    marques_preferees = serializers.ListField()
    prix_moyen_consulte = serializers.FloatField()
    activite_recente = serializers.ListField()


class RechercheSuggestionSerializer(serializers.Serializer):
    """Sérialiseur pour les suggestions de recherche"""
    marques = serializers.ListField(child=serializers.CharField())
    modeles = serializers.ListField(child=serializers.CharField())
    villes = serializers.ListField(child=serializers.CharField())
