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
