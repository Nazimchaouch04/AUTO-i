@echo off
chcp 65001 > nul
echo.
echo  =========================================
echo   AutoIntel Backend v2.0 — Demarrage
echo  =========================================
echo.

set BACKEND=C:\Users\PC DZ\Desktop\AUTO-P\.claude\worktrees\compassionate-lamarr\backend
cd /d "%BACKEND%"

echo [1/3] Migrations en cours...
python manage.py migrate --run-syncdb
if errorlevel 1 (
    echo ERREUR: migrate a echoue. Verifiez Python/Django.
    pause
    exit /b 1
)

echo.
echo [2/3] Verification superuser...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@autointel.com', 'AutoIntel2024\!')
    print('  Superuser admin cree (mot de passe: AutoIntel2024\!)')
else:
    print('  Superuser admin existe deja')
"

echo.
echo [3/3] Lancement du serveur...
echo.
echo  Acces :
echo    API Root  : http://localhost:8000/
echo    Admin     : http://localhost:8000/admin/
echo    Health    : http://localhost:8000/api/health/
echo    API Auth  : http://localhost:8000/api-auth/
echo.
echo  Identifiants admin : admin / AutoIntel2024\!
echo.
python manage.py runserver 0.0.0.0:8000
