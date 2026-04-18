@echo off
chcp 65001 > nul
echo.
echo  =========================================
echo   AutoIntel — Backend Principal
echo  =========================================
echo.

set BACKEND=C:\Users\PC DZ\Desktop\AUTO-P\backend
cd /d "%BACKEND%"

set DJANGO_SETTINGS_MODULE=autointel.settings.development

echo [1/4] Installation des dependances...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo AVERTISSEMENT: pip install a rencontre une erreur.
)

echo.
echo [2/4] Migrations...
python manage.py migrate --run-syncdb
if errorlevel 1 (
    echo ERREUR: migrate a echoue.
    pause
    exit /b 1
)

echo.
echo [3/4] Verification superuser...
python -c "
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'autointel.settings.development'
django.setup()
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@autointel.com', 'AutoIntel2024')
    print('  Superuser admin cree (mdp: AutoIntel2024)')
else:
    print('  Superuser admin deja present')
"

echo.
echo [4/4] Demarrage du serveur...
echo  Backend: http://localhost:8000
echo  Admin:   http://localhost:8000/admin/
echo.
python manage.py runserver 0.0.0.0:8000

pause
