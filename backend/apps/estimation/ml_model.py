import os
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / 'ml_models' / 'prix_model.pkl'
ENCODERS_PATH = BASE_DIR / 'ml_models' / 'encoders.pkl'

MARQUES_BASE_PRIX = {
    'Renault': 12000, 'Peugeot': 13000, 'Volkswagen': 18000,
    'Toyota': 16000, 'Dacia': 9000, 'Ford': 14000,
    'BMW': 28000, 'Mercedes': 32000, 'Hyundai': 15000,
    'Kia': 14000, 'Citroën': 11000, 'Opel': 12500,
    'Nissan': 15000, 'Fiat': 11000, 'Seat': 13500,
}

class ModeleEstimationPrix:
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.is_trained = False

    def generer_donnees_synthetiques(self, n=2000):
        import random
        marques = list(MARQUES_BASE_PRIX.keys())
        carburants = ['essence', 'diesel', 'electrique', 'hybride']
        boites = ['manuelle', 'automatique']
        pays = ['DZ', 'TN', 'FR', 'MA']
        rows = []
        for _ in range(n):
            marque = random.choice(marques)
            annee = random.randint(2005, 2024)
            km = random.randint(5000, 350000)
            carburant = random.choice(carburants)
            boite = random.choice(boites)
            puissance = random.randint(60, 400)
            pays_v = random.choice(pays)
            age = 2025 - annee
            prix_base = MARQUES_BASE_PRIX.get(marque, 15000)
            prix = prix_base
            prix *= max(0.25, 1 - age * 0.065)
            prix *= max(0.45, 1 - km / 350000)
            prix *= {'electrique': 1.18, 'hybride': 1.10,
                     'essence': 1.0, 'diesel': 0.96}.get(carburant, 1.0)
            prix *= 1.0 + (puissance - 100) * 0.0008
            prix *= {'automatique': 1.07, 'manuelle': 1.0}.get(boite, 1.0)
            prix *= random.uniform(0.88, 1.12)
            rows.append({
                'marque': marque, 'annee': annee,
                'kilometrage': km, 'carburant': carburant,
                'boite': boite, 'puissance': puissance,
                'pays': pays_v, 'prix': round(prix, 2)
            })
        return pd.DataFrame(rows)

    def preparer_features(self, df):
        df = df.copy()
        df['age'] = 2025 - df['annee']
        df['log_km'] = np.log1p(df['kilometrage'])
        df['km_par_an'] = df['kilometrage'] / (df['age'] + 1)
        cat_cols = ['marque', 'carburant', 'boite', 'pays']
        for col in cat_cols:
            enc_key = f'{col}_enc'
            if col not in self.encoders:
                self.encoders[col] = LabelEncoder()
                df[enc_key] = self.encoders[col].fit_transform(df[col].fillna('inconnu'))
            else:
                known = set(self.encoders[col].classes_)
                df[col] = df[col].apply(lambda x: x if x in known else 'inconnu')
                if 'inconnu' not in known:
                    self.encoders[col].classes_ = np.append(self.encoders[col].classes_, 'inconnu')
                df[enc_key] = self.encoders[col].transform(df[col].fillna('inconnu'))
        feature_cols = ['age', 'log_km', 'km_par_an', 'puissance',
                        'marque_enc', 'carburant_enc', 'boite_enc', 'pays_enc']
        return df[feature_cols]

    def entrainer(self):
        try:
            from apps.annonces.models import Annonce
            annonces = Annonce.objects.filter(
                est_active=True, prix__gt=500, prix__lt=200000
            ).values('marque__nom', 'annee', 'kilometrage',
                     'carburant', 'boite', 'puissance', 'pays', 'prix')
            df_reel = pd.DataFrame(list(annonces))
            if not df_reel.empty:
                df_reel = df_reel.rename(columns={'marque__nom': 'marque'})
                df_reel['puissance'] = df_reel['puissance'].fillna(100)
        except Exception:
            df_reel = pd.DataFrame()
            
        n_synth = max(500, 2000 - len(df_reel))
        df_synth = self.generer_donnees_synthetiques(n_synth)
        df = pd.concat([df_reel, df_synth], ignore_index=True)
        X = self.preparer_features(df)
        y = df['prix']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)
        self.model = GradientBoostingRegressor(
            n_estimators=300, max_depth=5,
            learning_rate=0.08, random_state=42,
            subsample=0.8, min_samples_leaf=5)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        os.makedirs(MODEL_PATH.parent, exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.encoders, ENCODERS_PATH)
        self.is_trained = True
        print(f"Modèle entraîné | MAE: {mae:.0f}€ | R²: {r2:.3f}")
        return {'mae': round(mae), 'r2': round(r2, 3), 'n_samples': len(df)}

    def charger(self):
        if MODEL_PATH.exists() and ENCODERS_PATH.exists():
            self.model = joblib.load(MODEL_PATH)
            self.encoders = joblib.load(ENCODERS_PATH)
            self.is_trained = True
            return True
        return False

    def estimer(self, marque, annee, kilometrage, carburant, boite, puissance, pays):
        if not self.is_trained:
            if not self.charger():
                self.entrainer()
        df = pd.DataFrame([{
            'marque': marque, 'annee': annee,
            'kilometrage': kilometrage, 'carburant': carburant,
            'boite': boite, 'puissance': puissance or 100, 'pays': pays
        }])
        X = self.preparer_features(df)
        prix = float(self.model.predict(X)[0])
        feature_names = ['Âge', 'Kilométrage (log)', 'Km/an',
                         'Puissance', 'Marque', 'Carburant', 'Boîte', 'Pays']
        importances = self.model.feature_importances_
        facteurs = []
        for name, imp in sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)[:3]:
            facteurs.append({'label': name, 'poids': round(imp * 100, 1)})
        return {
            'prix_estime': round(prix / 100) * 100,
            'fourchette_basse': round(prix * 0.87 / 100) * 100,
            'fourchette_haute': round(prix * 1.13 / 100) * 100,
            'fiabilite': 'haute' if prix > 3000 else 'moyenne',
            'facteurs': facteurs,
        }

_modele = ModeleEstimationPrix()

def get_modele():
    global _modele
    if not _modele.is_trained:
        _modele.charger() or _modele.entrainer()
    return _modele
