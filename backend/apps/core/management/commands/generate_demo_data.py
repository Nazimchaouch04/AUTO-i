#!/usr/bin/env python
"""
Génère des données de démo réalistes pour tester l'admin AutoIntel
"""
import random
from datetime import datetime, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from apps.annonces.models import Marque, Annonce
from apps.users.models import UserProfile
from apps.subscriptions.models import Plan, Abonnement
from apps.alertes.models import Alerte
from apps.estimation.models import EstimationHistory


class Command(BaseCommand):
    help = 'Génère des données de démo pour tester le back-office AutoIntel'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Génération des données de démo...'))

        # 1. Créer les marques
        self.create_marques()

        # 2. Créer les plans si non existants
        self.create_plans()

        # 3. Créer les utilisateurs de test
        self.create_users()

        # 4. Créer des annonces réalistes
        self.create_annonces()

        # 5. Créer des alertes
        self.create_alertes()

        # 6. Créer des estimations
        self.create_estimations()

        self.stdout.write(self.style.SUCCESS('\n✅ Données de démo générées avec succès !'))
        self.stdout.write(self.style.NOTICE('\n📊 Résumé :'))
        self.stdout.write(f"   • Marques : {Marque.objects.count()}")
        self.stdout.write(f"   • Annonces : {Annonce.objects.count()}")
        self.stdout.write(f"   • Utilisateurs : {User.objects.count() - 1}")  # -1 pour admin
        self.stdout.write(f"   • Alertes : {Alerte.objects.count()}")
        self.stdout.write(f"   • Estimations : {EstimationHistory.objects.count()}")

    def create_marques(self):
        marques_data = [
            ('Renault', 'renault', True),
            ('Peugeot', 'peugeot', True),
            ('Volkswagen', 'volkswagen', True),
            ('BMW', 'bmw', True),
            ('Mercedes', 'mercedes', True),
            ('Audi', 'audi', True),
            ('Toyota', 'toyota', True),
            ('Hyundai', 'hyundai', True),
            ('Kia', 'kia', False),
            ('Dacia', 'dacia', True),
            ('Citroën', 'citroen', False),
            ('Ford', 'ford', False),
            ('Nissan', 'nissan', False),
            ('Seat', 'seat', False),
        ]

        for nom, slug, populaire in marques_data:
            Marque.objects.get_or_create(
                slug=slug,
                defaults={'nom': nom, 'populaire': populaire}
            )
        self.stdout.write(f"   ✓ {len(marques_data)} marques créées")

    def create_plans(self):
        plans = [
            {'nom': 'free', 'prix_mensuel': 0, 'estimations_par_mois': 5, 'alertes_max': 2},
            {'nom': 'pro', 'prix_mensuel': 990, 'estimations_par_mois': 50, 'alertes_max': 20},
            {'nom': 'business', 'prix_mensuel': 9900, 'estimations_par_mois': 200, 'alertes_max': 100},
        ]
        for plan_data in plans:
            Plan.objects.get_or_create(
                nom=plan_data['nom'],
                defaults=plan_data
            )
        self.stdout.write(f"   ✓ {len(plans)} plans d'abonnement créés")

    def create_users(self):
        users_data = [
            {'username': 'client1', 'email': 'client1@example.com', 'password': 'test123', 'plan': 'free'},
            {'username': 'client2', 'email': 'client2@example.com', 'password': 'test123', 'plan': 'pro'},
            {'username': 'client3', 'email': 'client3@example.com', 'password': 'test123', 'plan': 'business'},
            {'username': 'ahmed', 'email': 'ahmed@example.com', 'password': 'test123', 'plan': 'pro'},
            {'username': 'fatima', 'email': 'fatima@example.com', 'password': 'test123', 'plan': 'free'},
        ]

        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password']
                )
                # Le signal créera automatiquement le profil et l'abonnement free
                # Mais on met à jour l'abonnement selon le plan choisi
                plan = Plan.objects.get(nom=user_data['plan'])
                abonnement, _ = Abonnement.objects.get_or_create(
                    user=user,
                    defaults={'plan': plan, 'actif': True}
                )
                if abonnement.plan != plan:
                    abonnement.plan = plan
                    abonnement.save()

                # Ajouter des coins et XP aléatoires pour la démo
                profile = user.profile
                profile.coins = random.randint(50, 500)
                profile.xp = random.randint(0, 5000)
                profile.level = random.randint(1, 5)
                profile.country = random.choice(['DZ', 'TN', 'MA', 'FR'])
                profile.save()

        self.stdout.write(f"   ✓ {len(users_data)} utilisateurs de test créés")

    def create_annonces(self):
        marques = list(Marque.objects.all())
        modeles = {
            'Renault': ['Clio', 'Megane', 'Duster', 'Captur', 'Talisman'],
            'Peugeot': ['208', '308', '3008', '5008', '2008'],
            'Volkswagen': ['Golf', 'Polo', 'Tiguan', 'Passat', 'T-Roc'],
            'BMW': ['Série 1', 'Série 3', 'Série 5', 'X1', 'X3', 'X5'],
            'Mercedes': ['Classe A', 'Classe C', 'Classe E', 'GLA', 'GLC'],
            'Audi': ['A1', 'A3', 'A4', 'A5', 'Q3', 'Q5'],
            'Toyota': ['Yaris', 'Corolla', 'C-HR', 'RAV4', 'Camry'],
            'Hyundai': ['i10', 'i20', 'i30', 'Tucson', 'Santa Fe'],
            'Kia': ['Picanto', 'Rio', 'Ceed', 'Sportage', 'Sorento'],
            'Dacia': ['Sandero', 'Duster', 'Logan', 'Spring', 'Jogger'],
            'Citroën': ['C3', 'C4', 'C5 Aircross', 'Berlingo'],
            'Ford': ['Fiesta', 'Focus', 'Puma', 'Kuga', 'Mondeo'],
            'Nissan': ['Micra', 'Juke', 'Qashqai', 'X-Trail', 'Leaf'],
            'Seat': ['Ibiza', 'Leon', 'Arona', 'Ateca', 'Tarraco'],
        }
        carburants = ['essence', 'diesel', 'electrique', 'hybride']
        boites = ['manuelle', 'automatique']
        pays_list = ['DZ', 'TN', 'MA', 'FR']
        villes = {
            'DZ': ['Alger', 'Oran', 'Constantine', 'Annaba', 'Blida'],
            'TN': ['Tunis', 'Sfax', 'Sousse', 'Kairouan', 'Bizerte'],
            'MA': ['Casablanca', 'Rabat', 'Marrakech', 'Fès', 'Tanger'],
            'FR': ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice'],
        }

        # Supprimer les anciennes annonces de démo pour éviter les doublons
        Annonce.objects.filter(source='demo').delete()

        annonces_crees = 0
        for _ in range(50):  # Créer 50 annonces
            marque = random.choice(marques)
            modele = random.choice(modeles.get(marque.nom, ['Standard']))
            annee = random.randint(2015, 2024)
            km = random.randint(10000, 200000)
            carburant = random.choice(carburants)
            boite = random.choice(boites)
            pays = random.choice(pays_list)
            ville = random.choice(villes[pays])

            # Prix de base selon l'année et la marque
            prix_base = random.randint(15000, 80000) if annee >= 2020 else random.randint(8000, 40000)
            if marque.nom in ['BMW', 'Mercedes', 'Audi']:
                prix_base = int(prix_base * 1.5)

            # Prix estimé (ML) avec une variation
            prix_estime = int(prix_base * random.uniform(0.85, 1.15))
            ecart = ((prix_base - prix_estime) / prix_estime) * 100 if prix_estime else 0

            # Déterminer si c'est une bonne affaire
            est_bonne_affaire = ecart <= -10
            score_affaire = max(0, min(100, int(abs(ecart) * 2)))

            annonce = Annonce.objects.create(
                marque=marque,
                modele=modele,
                annee=annee,
                kilometrage=km,
                carburant=carburant,
                boite=boite,
                puissance=random.randint(90, 300),
                prix=Decimal(prix_base),
                prix_estime=Decimal(prix_estime) if random.random() > 0.2 else None,
                ecart_prix=round(ecart, 1) if prix_estime else None,
                score_affaire=score_affaire,
                est_bonne_affaire=est_bonne_affaire,
                ville=ville,
                pays=pays,
                source='demo',
                description=f"{marque.nom} {modele} {annee} - {km}km - {carburant} - {boite}",
                est_active=random.random() > 0.1,  # 90% actives
                date_publication=timezone.now() - timedelta(days=random.randint(0, 30)),
            )
            annonces_crees += 1

        self.stdout.write(f"   ✓ {annonces_crees} annonces créées")

    def create_alertes(self):
        users = list(User.objects.filter(username__startswith='client'))
        if not users:
            return

        Alerte.objects.filter(user__in=users).delete()

        alertes_crees = 0
        for user in users[:3]:  # Créer des alertes pour 3 utilisateurs
            for i in range(random.randint(1, 3)):
                Alerte.objects.create(
                    user=user,
                    titre=f"Alerte {user.username} #{i+1}",
                    marque=random.choice(['Renault', 'Peugeot', 'BMW', '']),
                    modele=random.choice(['Clio', '308', 'Série 3', '']),
                    prix_min=random.randint(10000, 30000) if random.random() > 0.5 else None,
                    prix_max=random.randint(40000, 100000) if random.random() > 0.5 else None,
                    km_max=random.randint(50000, 150000) if random.random() > 0.5 else None,
                    annee_min=random.randint(2015, 2020) if random.random() > 0.5 else None,
                    carburant=random.choice(['essence', 'diesel', '']),
                    pays=random.choice(['DZ', 'TN', 'MA']),
                    est_active=True,
                )
                alertes_crees += 1

        self.stdout.write(f"   ✓ {alertes_crees} alertes créées")

    def create_estimations(self):
        users = list(User.objects.all())
        if not users:
            return

        EstimationHistory.objects.filter(user__in=users).delete()

        estimations_crees = 0
        for _ in range(30):  # 30 estimations
            user = random.choice(users)
            marque = random.choice(['Renault', 'Peugeot', 'BMW', 'Audi', 'Toyota'])
            modele = random.choice(['Clio', '308', 'Série 3', 'A4', 'Corolla'])
            annee = random.randint(2015, 2024)

            prix_estime = random.randint(15000, 80000)
            fourchette_basse = int(prix_estime * 0.9)
            fourchette_haute = int(prix_estime * 1.1)

            EstimationHistory.objects.create(
                user=user,
                marque=marque,
                modele=modele,
                annee=annee,
                kilometrage=random.randint(10000, 150000),
                carburant=random.choice(['essence', 'diesel', 'electrique']),
                boite=random.choice(['manuelle', 'automatique']),
                pays=random.choice(['DZ', 'TN', 'MA', 'FR']),
                prix_estime=Decimal(prix_estime),
                fourchette_basse=Decimal(fourchette_basse),
                fourchette_haute=Decimal(fourchette_haute),
                fiabilite=random.choice(['Haute', 'Moyenne', 'Basse']),
                nb_annonces_reference=random.randint(10, 100),
            )
            estimations_crees += 1

        self.stdout.write(f"   ✓ {estimations_crees} estimations créées")
