import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
import joblib, os, random
from pathlib import Path
from django.conf import settings

MODEL_DIR = Path(settings.BASE_DIR) / 'ml_models'
MODEL_PATH = MODEL_DIR / 'prix_model.pkl'
ENCODER_PATH = MODEL_DIR / 'encoders.pkl'

BASE_PRICES = {
    'Renault': 2000000, 'Peugeot': 2300000, 'Volkswagen': 3200000,
    'Toyota': 2900000, 'Dacia': 1600000, 'Ford': 2600000,
    'BMW': 5000000, 'Mercedes': 5500000, 'Hyundai': 2700000,
    'Kia': 2500000, 'Citroën': 2000000, 'Fiat': 1800000,
    'Opel': 2200000, 'Geely': 2400000, 'Chery': 2100000, 'Nissan': 2800000,
}

class PriceModel:
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.ready = False

    def _gen_synthetic(self, n=2000):
        rows = []
        brands = list(BASE_PRICES.keys())
        fuels = ['essence', 'diesel', 'electrique', 'hybride']
        boxes = ['manuelle', 'automatique']
        countries = ['DZ', 'TN', 'FR', 'MA']
        for _ in range(n):
            brand = random.choice(brands)
            year = random.randint(2005, 2024)
            km = random.randint(5000, 350000)
            fuel = random.choice(fuels)
            box = random.choice(boxes)
            power = random.randint(60, 400)
            country = random.choice(countries)
            age = 2025 - year
            base = BASE_PRICES[brand]
            price = base
            price *= max(0.2, 1 - age * 0.062)
            price *= max(0.4, 1 - km / 400000)
            price *= {
                'electrique': 1.20, 'hybride': 1.10,
                'essence': 1.0, 'diesel': 0.95
            }.get(fuel, 1.0)
            price *= 1.0 + (power - 100) * 0.0007
            price *= {
                'automatique': 1.07, 'manuelle': 1.0
            }.get(box, 1.0)
            price *= random.uniform(0.87, 1.13)
            rows.append({
                'marque': brand, 'annee': year, 'kilometrage': km,
                'carburant': fuel, 'boite': box, 'puissance': power,
                'pays': country, 'prix': round(price)
            })
        return pd.DataFrame(rows)

    def _prepare(self, df):
        df = df.copy()
        df['age'] = 2025 - df['annee']
        df['log_km'] = np.log1p(df['kilometrage'])
        df['km_an'] = df['kilometrage'] / (df['age'] + 1)
        for col in ['marque', 'carburant', 'boite', 'pays']:
            key = f'{col}_enc'
            if col not in self.encoders:
                self.encoders[col] = LabelEncoder()
                df[key] = self.encoders[col].fit_transform(
                    df[col].fillna('inconnu')
                )
            else:
                known = set(self.encoders[col].classes_)
                df[col] = df[col].apply(
                    lambda x: x if x in known else 'inconnu'
                )
                if 'inconnu' not in known:
                    self.encoders[col].classes_ = np.append(
                        self.encoders[col].classes_, 'inconnu'
                    )
                df[key] = self.encoders[col].transform(
                    df[col].fillna('inconnu')
                )
        feats = [
            'age', 'log_km', 'km_an', 'puissance',
            'marque_enc', 'carburant_enc', 'boite_enc', 'pays_enc'
        ]
        return df[feats]

    def train(self):
        MODEL_DIR.mkdir(exist_ok=True)
        try:
            from apps.annonces.models import Annonce
            qs = Annonce.objects.filter(
                est_active=True, prix__gt=200000, prix__lt=30000000
            ).values(
                'marque__nom', 'annee', 'kilometrage',
                'carburant', 'boite', 'puissance', 'pays', 'prix'
            )
            df_real = pd.DataFrame(list(qs))
            if not df_real.empty:
                df_real = df_real.rename(
                    columns={'marque__nom': 'marque'}
                )
                df_real['puissance'] = df_real['puissance'].fillna(100)
        except Exception:
            df_real = pd.DataFrame()

        n = max(500, 2000 - len(df_real))
        df = pd.concat([df_real, self._gen_synthetic(n)], ignore_index=True)
        X = self._prepare(df)
        y = df['prix']
        self.model = GradientBoostingRegressor(
            n_estimators=300, max_depth=5,
            learning_rate=0.08, random_state=42,
            subsample=0.8
        )
        self.model.fit(X, y)
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.encoders, ENCODER_PATH)
        self.ready = True
        return {'samples': len(df)}

    def load(self):
        if MODEL_PATH.exists() and ENCODER_PATH.exists():
            self.model = joblib.load(MODEL_PATH)
            self.encoders = joblib.load(ENCODER_PATH)
            self.ready = True
            return True
        return False

    def estimate(self, marque, annee, kilometrage, carburant,
                 boite, puissance, pays):
        if not self.ready:
            if not self.load():
                self.train()
        df = pd.DataFrame([{
            'marque': marque, 'annee': annee, 'kilometrage': kilometrage,
            'carburant': carburant, 'boite': boite,
            'puissance': puissance or 100, 'pays': pays,
        }])
        X = self._prepare(df)
        px = float(self.model.predict(X)[0])

        # Comparable count
        try:
            from apps.annonces.models import Annonce
            comparable = Annonce.objects.filter(
                marque__nom__iexact=marque,
                annee__range=(annee-2, annee+2),
                carburant=carburant, pays=pays, est_active=True
            ).count()
        except Exception:
            comparable = 0

        return {
            'estimated_price': round(px / 1000) * 1000,
            'confidence_low': round(px * 0.87 / 1000) * 1000,
            'confidence_high': round(px * 1.13 / 1000) * 1000,
            'reliability': 'haute' if px > 500000 else 'moyenne',
            'comparable_count': comparable,
        }

_model_instance = PriceModel()

def get_model():
    global _model_instance
    if not _model_instance.ready:
        _model_instance.load() or _model_instance.train()
    return _model_instance
