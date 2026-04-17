@echo off
echo ============================================
echo   LANCEMENT BACKEND - Python 3.11
echo ============================================
echo.
cd /d "C:\Users\PC DZ\Desktop\AUTO-P\backend"
echo Repertoire: %CD%
echo.
echo Lancement du serveur Django...
.venv311\Scripts\python.exe manage.py runserver 127.0.0.1:8000
echo.
pause
