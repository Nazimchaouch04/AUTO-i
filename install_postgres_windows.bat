@echo off
echo === Installation PostgreSQL pour AutoIntel ===

REM Vérifier si Chocolatey est installé
choco --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Chocolatey n'est pas installé. Installation en cours...
    powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
)

REM Installer PostgreSQL
echo Installation de PostgreSQL...
choco install postgresql --yes

REM Démarrer le service PostgreSQL
echo Démarrage du service PostgreSQL...
net start postgresql-x64-15

REM Créer la base de données
echo Création de la base de données autointel_db...
createdb -U postgres autointel_db

echo Installation terminée!
echo PostgreSQL est maintenant installé et configuré.
echo Vous pouvez maintenant lancer: python migrate_to_postgres.py
pause
