@echo off
echo ============================================
echo   LANCEMENT AUTINTEL - Backend + Frontend
echo ============================================
echo.

:: Lancer le Backend Django (port 8000)
echo [1/2] Lancement du Backend Django sur http://127.0.0.1:8000 ...
cd /d "C:\Users\PC DZ\Desktop\AUTO-P\backend"
start "Backend Django" cmd /k "python manage.py runserver 0.0.0.0:8000"

:: Attendre 3 secondes
ping 127.0.0.1 -n 4 > nul

:: Lancer le Frontend Vite (port 5173)
echo [2/2] Lancement du Frontend Vite sur http://localhost:5173 ...
cd /d "C:\Users\PC DZ\Desktop\AUTO-P\frontend"
start "Frontend Vite" cmd /k "npm run dev"

echo.
echo ============================================
echo   SERVEURS LANCEES !
echo ============================================
echo.
echo Backend API:  http://127.0.0.1:8000
echo Admin:        http://127.0.0.1:8000/admin/
echo Frontend:     http://localhost:5173
echo.
echo Pour arreter : fermez les fenetres CMD ouvertes
echo.
pause
