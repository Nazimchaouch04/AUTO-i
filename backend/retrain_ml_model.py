#!/usr/bin/env python
"""
Script pour réentraîner le modèle ML d'estimation
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.estimation.ml_model import get_modele

print("=" * 60)
print("RÉENTRAÎNEMENT DU MODÈLE ML")
print("=" * 60)

try:
    modele = get_modele()
    print(f"Modèle chargé: {modele.is_trained}")
    
    print("\n🔄 Entraînement en cours...")
    result = modele.entrainer()
    
    print("\n✅ Entraînement terminé avec succès!")
    print(f"📊 Résultats:")
    print(f"   - MAE (Erreur moyenne): {result['mae']}€")
    print(f"   - R² (Score): {result['r2']}")
    print(f"   - Échantillons: {result['n_samples']}")
    print(f"\n💾 Modèle sauvegardé dans: ml_models/prix_model.pkl")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Erreur lors de l'entraînement: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
