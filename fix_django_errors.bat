@echo off
echo 🔧 Correction des erreurs Django Admin - Python 3.14
echo.

cd backend

echo 📦 Mise a jour des dependances...
pip install -r requirements.txt --upgrade

echo 🗄️ Nettoyage de la base de donnees...
if exist db.sqlite3 del db.sqlite3

echo 🔄 Creation des migrations...
python manage.py makemigrations

echo 📋 Application des migrations...
python manage.py migrate

echo 👤 Creation du super-utilisateur...
python manage.py createsuperuser

echo 🚀 Demarrage du serveur...
python manage.py runserver

echo.
echo ✅ Corrections appliquees avec succes!
echo 🌐 Acces: http://localhost:8000/admin/
echo 📚 Documentation: FIX_DJANGO_ERRORS.md
echo.
pause
