from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.utils import timezone


def _database_health():
    """Lightweight DB ping used by health endpoint."""
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
        return {'ok': True, 'detail': 'database reachable'}
    except OperationalError as exc:
        return {'ok': False, 'detail': str(exc)}


def api_root(request):
    return JsonResponse(
        {
            'message': 'AutoIntel API',
            'backend': 'OK',
            'timestamp': timezone.now().isoformat(),
            'frontend': 'http://127.0.0.1:5173',
            'endpoints': [
                '/api/health/',
                '/api/auth/login/',
                '/api/auth/register/',
                '/api/auth/profile/',
                '/api/annonces/',
                '/api/estimation/',
                '/api/dashboard/',
                '/api/alertes/',
                '/api/subscriptions/',
                '/api/gamification/',
            ],
        }
    )


def api_health(request):
    db_status = _database_health()
    ok = db_status['ok']
    status_code = 200 if ok else 503

    return JsonResponse(
        {
            'status': 'ok' if ok else 'degraded',
            'database': db_status,
            'timestamp': timezone.now().isoformat(),
        },
        status=status_code,
    )
