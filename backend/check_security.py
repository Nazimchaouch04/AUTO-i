#!/usr/bin/env python
"""
Script de vérification de la sécurité Django
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.conf import settings

print("=" * 60)
print("🔍 VÉRIFICATION DE SÉCURITÉ - AUTO-P")
print("=" * 60)

issues = []
warnings = []
passes = []

# 1. DEBUG mode
if settings.DEBUG:
    issues.append("❌ DEBUG=True - Désactivez en production!")
else:
    passes.append("✅ DEBUG=False")

# 2. SECRET_KEY
if 'insecure' in settings.SECRET_KEY.lower() or 'change' in settings.SECRET_KEY.lower():
    issues.append("❌ SECRET_KEY par défaut - Changez-la!")
else:
    passes.append("✅ SECRET_KEY personnalisé")

# 3. ALLOWED_HOSTS
if settings.ALLOWED_HOSTS == ['*']:
    issues.append("❌ ALLOWED_HOSTS=['*'] - Spécifiez les domaines!")
elif not settings.ALLOWED_HOSTS:
    warnings.append("⚠️  ALLOWED_HOSTS vide - Ajoutez vos domaines")
else:
    passes.append(f"✅ ALLOWED_HOSTS configuré: {settings.ALLOWED_HOSTS}")

# 4. JWT Configuration
jwt_config = settings.SIMPLE_JWT
access_lifetime = jwt_config.get('ACCESS_TOKEN_LIFETIME').total_seconds() / 60
refresh_lifetime = jwt_config.get('REFRESH_TOKEN_LIFETIME').total_seconds() / 3600

if access_lifetime > 30:
    issues.append(f"❌ Access token trop long: {access_lifetime} min (max 30)")
else:
    passes.append(f"✅ Access token: {access_lifetime} min")

if refresh_lifetime > 24:
    warnings.append(f"⚠️  Refresh token long: {refresh_lifetime}h (recommandé: 24h)")
else:
    passes.append(f"✅ Refresh token: {refresh_lifetime}h")

if not jwt_config.get('ROTATE_REFRESH_TOKENS'):
    issues.append("❌ ROTATE_REFRESH_TOKENS=False - Activez-le!")
else:
    passes.append("✅ ROTATE_REFRESH_TOKENS=True")

if not jwt_config.get('BLACKLIST_AFTER_ROTATION'):
    warnings.append("⚠️  BLACKLIST_AFTER_ROTATION non activé")
else:
    passes.append("✅ BLACKLIST_AFTER_ROTATION=True")

# 5. Rate Limiting
throttle_rates = settings.REST_FRAMEWORK.get('DEFAULT_THROTTLE_RATES', {})
if not throttle_rates:
    issues.append("❌ Pas de rate limiting configuré!")
else:
    passes.append("✅ Rate limiting configuré")
    for rate_name, rate_limit in throttle_rates.items():
        passes.append(f"   - {rate_name}: {rate_limit}")

# 6. CORS
cors_origins = settings.CORS_ALLOWED_ORIGINS
if cors_origins == ['*'] or '*' in cors_origins:
    issues.append("❌ CORS autorise tous les origins!")
else:
    passes.append(f"✅ CORS restreint: {len(cors_origins)} origins")

# 7. Security Headers (en production)
if not settings.DEBUG:
    if not hasattr(settings, 'SECURE_SSL_REDIRECT'):
        issues.append("❌ SECURE_SSL_REDIRECT non configuré")
    else:
        passes.append("✅ SECURE_SSL_REDIRECT configuré")
    
    if not hasattr(settings, 'SECURE_HSTS_SECONDS'):
        warnings.append("⚠️  HSTS non configuré")
    else:
        passes.append("✅ HSTS configuré")
else:
    warnings.append("⚠️  Mode développement - headers de sécurité non appliqués")

# 8. Password Validators
password_validators = settings.AUTH_PASSWORD_VALIDATORS
if len(password_validators) < 3:
    warnings.append("⚠️  Peu de validateurs de mot de passe")
else:
    passes.append(f"✅ {len(password_validators)} validateurs de mot de passe")

# 9. Database
db_engine = settings.DATABASES['default']['ENGINE']
if 'sqlite' in db_engine:
    warnings.append("⚠️  SQLite utilisé en développement")
else:
    passes.append("✅ Base de données PostgreSQL")

# Affichage des résultats
print("\n✅ PASSES:")
for item in passes:
    print(f"  {item}")

print("\n⚠️  WARNINGS:")
for item in warnings:
    print(f"  {item}")

print("\n❌ ISSUES CRITIQUES:")
for item in issues:
    print(f"  {item}")

# Résumé
print("\n" + "=" * 60)
total_issues = len(issues)
total_warnings = len(warnings)
total_passes = len(passes)

if total_issues == 0 and total_warnings == 0:
    print("🎉 Configuration sécurisée!")
elif total_issues == 0:
    print(f"✅ Pas d'issues critiques ({total_warnings} avertissements)")
else:
    print(f"⚠️  {total_issues} issues critiques à corriger!")

print(f"Passes: {total_passes} | Warnings: {total_warnings} | Issues: {total_issues}")
print("=" * 60)

# Exit code
sys.exit(1 if total_issues > 0 else 0)
