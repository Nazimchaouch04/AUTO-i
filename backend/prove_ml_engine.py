import os
import django
import decimal
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()

from apps.estimation.ml_model import ModeleEstimationPrix

def prove_ml():
    print("🔬 TESTING AUTOINTEL ML ESTIMATION ENGINE...")
    ml = ModeleEstimationPrix()
    
    # Test cases: Case 1 (Common), Case 2 (Premium), Case 3 (Old/High-mileage)
    test_cars = [
        {'marque': 'Renault', 'modele': 'Clio', 'annee': 2019, 'kilometrage': 60000, 'carburant': 'essence', 'boite': 'manuelle', 'pays': 'DZ'},
        {'marque': 'Mercedes', 'modele': 'Classe-C', 'annee': 2022, 'kilometrage': 15000, 'carburant': 'diesel', 'boite': 'automatique', 'pays': 'DZ'},
        {'marque': 'Dacia', 'modele': 'Logan', 'annee': 2012, 'kilometrage': 250000, 'carburant': 'diesel', 'boite': 'manuelle', 'pays': 'DZ'},
    ]
    
    for i, car in enumerate(test_cars, 1):
        try:
            res = ml.estimer(
                marque=car['marque'],
                annee=car['annee'],
                kilometrage=car['kilometrage'],
                carburant=car['carburant'],
                boite=car['boite'],
                puissance=100,  # Default
                pays=car['pays']
            )
            print(f"\n🚗 CAR #{i}: {car['marque']} {car['modele']} ({car['annee']})")
            print(f"💰 ESTIMATED PRICE: {float(res['prix_estime']):,.2f} EUR")
            print(f"📉 RANGE: {float(res['fourchette_basse']):,.2f} - {float(res['fourchette_haute']):,.2f} EUR")
            print(f"🛡️ RELIABILITY: {res['fiabilite']}")
            print(f"📊 TOP FACTORS: {', '.join([f'{f['label']} ({f['poids']}%)' for f in res['facteurs']])}")
        except Exception as e:
            import traceback
            print(f"❌ Error predicting car {i}: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    prove_ml()
