@echo off
echo 🚀 Test configuration AutoIntel Backend...
echo.

REM Ajouter le chemin du backend au PYTHONPATH
set PYTHONPATH=%CD%\backend;%PYTHONPATH%

cd backend

echo 🔍 Configuration Django...
set DJANGO_SETTINGS_MODULE=autointel.settings

echo ✅ Test imports...
python -c "import sys; sys.path.insert(0, '.'); import django; django.setup(); print('Configuration Django OK')"

echo.
echo 🎉 Test termine!
echo.
echo 🚀 Maintenant executez:
echo 1. python manage.py makemigrations
echo 2. python manage.py migrate
echo 3. python manage.py createsuperuser
echo 4. python manage.py runserver
echo.
pause
