@echo off
chcp 65001 > nul
set BACKEND=C:\Users\PC DZ\Desktop\AUTO-P\.claude\worktrees\compassionate-lamarr\backend
cd /d "%BACKEND%"
echo Migration en cours...
python manage.py migrate --run-syncdb
echo.
echo Creation superuser admin...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@autointel.com', 'AutoIntel2024\!')
    print('Superuser admin cree')
else:
    print('Superuser admin existe deja')
"
echo Done.
pause
