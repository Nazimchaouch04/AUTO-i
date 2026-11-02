import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('autointel')


class SlowRequestLogMiddleware(MiddlewareMixin):
    THRESHOLD_MS = 500

    def process_request(self, request):
        request._t0 = time.time()

    def process_response(self, request, response):
        if hasattr(request, '_t0'):
            ms = round((time.time() - request._t0) * 1000)
            if ms > self.THRESHOLD_MS:
                user = getattr(request, 'user', None)
                u = user.username if user and user.is_authenticated else 'anon'
                logger.warning(
                    f"SLOW [{ms}ms] {request.method} {request.path} "
                    f"user={u} status={response.status_code}"
                )
        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware pour ajouter des headers de sécurité HTTP
    """
    def process_response(self, request, response):
        # Protection XSS
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Protection clickjacking
        response['X-Frame-Options'] = 'DENY'
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy (restreindre l'accès aux APIs sensibles)
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=(), payment=()'
        
        # Content Security Policy (en production uniquement)
        from django.conf import settings
        if not settings.DEBUG:
            response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
        
        return response
