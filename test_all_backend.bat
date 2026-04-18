@echo off
echo ============================================
echo   TEST BACKEND COMPLET - AutoIntel SaaS
echo ============================================
echo.

cd /d "C:\Users\PC DZ\Desktop\AUTO-P\backend"

echo [1/3] Activation venv...
call .venv311\Scripts\activate.bat

echo [2/3] Tests Django natifs...
python manage.py test --verbosity=2 --parallel

echo [3/3] Pytest avec coverage...
pytest --cov=apps --cov-report=html --cov-report=term -v

echo.
echo ============================================
echo   TESTS TERMINES ! Voir htmlcov/index.html
echo ============================================
pause

