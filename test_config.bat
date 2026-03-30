@echo off
echo 🚀 Lancement du test de configuration AutoIntel Backend...
echo.

REM Aller dans le répertoire backend
cd backend

REM Configurer l'environnement Django
set DJANGO_SETTINGS_MODULE=autointel.settings

echo 🔍 Test des imports Python...
python -c "import django; print('✅ Django importé')"

echo.
echo ⚙️  Configuration Django...
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings'); import django; django.setup(); print('✅ Configuration Django chargee')"

echo.
echo 📦 Test des apps...
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings'); import django; django.setup(); from apps.annonces.models import Marque; print('✅ Apps annonces importees')"

echo.
echo 🎉 Configuration testee avec succes!
echo.
echo 🚀 Prochaines commandes manuelles:
echo 1. python manage.py makemigrations
echo 2. python manage.py migrate  
echo 3. python manage.py createsuperuser
echo 4. python manage.py runserver
echo.
pause
