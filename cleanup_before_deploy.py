#!/usr/bin/env python
"""
Script pour nettoyer les fichiers de test et backup avant le déploiement
"""

import os
import shutil
from pathlib import Path

# Racine du projet
ROOT = Path(__file__).parent

# Fichiers et dossiers à supprimer
FILES_TO_DELETE = [
    # Fichiers de backup
    'backend/apps/ai_assistant/admin_old.py',
    'backend/apps/alertes/admin_old.py',
    'backend/apps/annonces/models_advanced.py',
    'backend/apps/annonces/serializers_advanced.py',
    'backend/apps/annonces/urls_advanced.py',
    'backend/apps/annonces/views_advanced.py',
    'backend/apps/annonces/views_old.py',
    'backend/apps/annonces/views_recommandations.py',
    'backend/apps/estimation/admin_old.py',
    'backend/apps/gamification/admin_old.py',
    'backend/apps/marketplace/admin_broken.py',
    'backend/apps/marketplace/admin_fixed.py',
    'backend/apps/marketplace/admin_old.py',
    'backend/apps/marketplace/models_broken.py',
    'backend/apps/marketplace/models_fixed.py',
    'backend/apps/marketplace/models_simple.py',
    'backend/apps/marketplace/services_simple.py',
    'backend/apps/marketplace/tests_fixed.py',
    'backend/apps/marketplace/urls_working.py',
    'backend/apps/notifications/admin_old.py',
    'backend/apps/notifications/email_service.py',
    'backend/apps/rapports/admin_old.py',
    'backend/apps/subscriptions/admin_old.py',
    'database/backend/apps/subscriptions/tests_fixed.py',
    'backend/apps/users/admin_old.py',
    'backend/apps/users/apps_init.py',
    'backend/apps/users/tests_fixed.py',
    'backend/autointel/settings/base.py',
    'backend/autointel/settings/development.py',
    'backend/autointel/tests_fixed.py',
    
    # Fichiers temporaires
    'backend/sqlite_data.json',
    'TODO.md',
    'TODO_TESTS.md',
    'test_config.py',
    'ADMIN_CREDENTIALS.md',
    'VERIFICATION_SUMMARY.md',
]

DIRS_TO_DELETE = [
    '.claude/worktrees',
]

print("=" * 60)
print("NETTOYAGE AVANT DÉPLOIEMENT")
print("=" * 60)

deleted_count = 0
for file_path in FILES_TO_DELETE:
    full_path = ROOT / file_path
    if full_path.exists():
        try:
            if full_path.is_file():
                full_path.unlink()
                print(f"✅ Supprimé: {file_path}")
                deleted_count += 1
        except Exception as e:
            print(f"❌ Erreur {file_path}: {e}")

for dir_path in DIRS_TO_DELETE:
    full_path = ROOT / dir_path
    if full_path.exists():
        try:
            shutil.rmtree(full_path)
            print(f"✅ Supprimé: {dir_path}")
            deleted_count += 1
        except Exception as e:
            print(f"❌ Erreur {dir_path}: {e}")

print("\n" + "=" * 60)
print(f"✅ Nettoyage terminé: {deleted_count} éléments supprimés")
print("=" * 60)
