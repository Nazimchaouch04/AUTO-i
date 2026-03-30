from apps.annonces.models import Vehicule, Annonce
from apps.gamification.models import Defi
from django.utils import timezone
from decimal import Decimal

# Crée les véhicules
VEHICLES = [
    ('Renault', 'Clio'),
    ('Renault', 'Megane'),
    ('Renault', 'Scenic'),
    ('Peugeot', '206'),
    ('Peugeot', '307'),
    ('Peugeot', '308'),
    ('Volkswagen', 'Golf'),
    ('Volkswagen', 'Polo'),
    ('Volkswagen', 'Passat'),
    ('Toyota', 'Corolla'),
    ('Toyota', 'Yaris'),
    ('Toyota', 'Camry'),
    ('Dacia', 'Sandero'),
    ('Dacia', 'Duster'),
    ('Dacia', 'Logan'),
    ('Ford', 'Fiesta'),
    ('Ford', 'Focus'),
    ('Ford', 'Mondeo'),
    ('BMW', '320'),
    ('BMW', '328'),
    ('BMW', 'X5'),
    ('Mercedes', 'C-Class'),
    ('Mercedes', 'E-Class'),
    ('Mercedes', 'GLE'),
    ('Hyundai', 'i20'),
    ('Hyundai', 'i30'),
    ('Hyundai', 'Tucson'),
    ('Kia', 'Picanto'),
    ('Kia', 'Ceed'),
    ('Kia', 'Sportage'),
]

# Crée les véhicules
for marque, modele in VEHICLES:
    Vehicule.objects.get_or_create(marque=marque, modele=modele, defaults={'categorie': 'berline'})

print(f"✓ {Vehicule.objects.count()} véhicules créés")

# Données pour les annonces réalistes
import random
from datetime import timedelta

CARBURANTS = ['essence', 'diesel', 'hybride', 'electrique']
BOITES = ['manuelle', 'automatique']
PAYS = ['DZ', 'TN', 'FR', 'MA']
VILLES_DZ = ['Alger', 'Oran', 'Constantine', 'Annaba', 'Algiers']
VILLES_FR = ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice']
VILLES_TN = ['Tunis', 'Sfax', 'Sousse', 'Kairouan', 'Gafsa']
VILLES_MA = ['Casablanca', 'Fez', 'Marrakech', 'Rabat', 'Tangier']

def get_ville(pays):
    if pays == 'DZ':
        return random.choice(VILLES_DZ)
    elif pays == 'FR':
        return random.choice(VILLES_FR)
    elif pays == 'TN':
        return random.choice(VILLES_TN)
    else:
        return random.choice(VILLES_MA)

# Crée 60 annonces réalistes
for i in range(60):
    vehicule = random.choice(Vehicule.objects.all())
    annee = random.randint(2015, 2024)
    km = random.randint(20000, 200000)
    carburant = random.choice(CARBURANTS)
    boite = random.choice(BOITES)
    pays = random.choice(PAYS)
    
    # Prix cohérents selon l'année et km
    age = 2025 - annee
    prix_base = {
        'Renault': 12000, 'Peugeot': 13000, 'Volkswagen': 18000,
        'Toyota': 16000, 'Dacia': 9000, 'Ford': 14000,
        'BMW': 28000, 'Mercedes': 32000, 'Hyundai': 15000, 'Kia': 14000,
    }.get(vehicule.marque, 13000)
    
    facteur_age = max(0.3, 1 - (age * 0.07))
    facteur_km = max(0.5, 1 - (km / 300000))
    facteur_carburant = {'electrique': 1.15, 'hybride': 1.08, 'essence': 1.0, 'diesel': 0.95}.get(carburant, 1.0)
    
    prix_estime = int(prix_base * facteur_age * facteur_km * facteur_carburant)
    prix_reel = prix_estime + random.randint(-3000, 5000)
    ecart = ((prix_reel - prix_estime) / prix_estime * 100) if prix_estime else 0
    est_bonne_affaire = ecart < -10
    score_affaire = max(0, -int(ecart)) if ecart < 0 else 0
    
    Annonce.objects.create(
        vehicule=vehicule,
        annee=annee,
        kilometrage=km,
        carburant=carburant,
        boite=boite,
        puissance=random.randint(80, 200),
        prix=Decimal(str(prix_reel)),
        prix_estime=Decimal(str(prix_estime)),
        ecart_prix=ecart,
        score_affaire=score_affaire,
        est_bonne_affaire=est_bonne_affaire,
        source='leboncoin',
        ville=get_ville(pays),
        pays=pays,
        description=f"{vehicule.marque} {vehicule.modele} {annee} en bon état, {km} km, {carburant}",
        est_active=True,
    )

print(f"✓ 60 annonces créées")

# Crée les défis
DEFIS_DATA = [
    {
        'titre': 'Première estimation',
        'description': 'Effectuez votre première estimation de prix',
        'type': 'quotidien', 'xp_reward': 50, 'ac_reward': 25, 'cible_count': 1
    },
    {
        'titre': 'Détecteur de bonnes affaires',
        'description': 'Trouvez 5 bonnes affaires',
        'type': 'hebdomadaire', 'xp_reward': 150, 'ac_reward': 75, 'cible_count': 5
    },
    {
        'titre': 'Expert automobile',
        'description': 'Effectuez 20 estimations dans le mois',
        'type': 'mensuel', 'xp_reward': 300, 'ac_reward': 200, 'cible_count': 20
    },
    {
        'titre': 'Légende AutoIntel',
        'description': 'Atteignez le niveau 6',
        'type': 'legendaire', 'xp_reward': 1000, 'ac_reward': 500, 'cible_count': 1
    },
]

for defi_data in DEFIS_DATA:
    Defi.objects.get_or_create(
        titre=defi_data['titre'],
        defaults=defi_data
    )

print(f"✓ {Defi.objects.count()} défis créés")
print("\n✅ Seed data complété !")
