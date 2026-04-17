from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging

logger = logging.getLogger('autointel')


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            'error': True,
            'status_code': response.status_code,
            'message': _extract_message(response.data),
            'details': response.data,
        }
    else:
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        response = Response({
            'error': True,
            'status_code': 500,
            'message': 'Erreur interne du serveur.',
        }, status=500)
    return response


def _extract_message(data):
    if isinstance(data, dict):
        for key in ('detail', 'non_field_errors', 'message'):
            if key in data:
                v = data[key]
                return str(v[0]) if isinstance(v, list) else str(v)
        first = next(iter(data.values()), '')
        return str(first[0]) if isinstance(first, list) else str(first)
    if isinstance(data, list) and data:
        return str(data[0])
    return 'Erreur de validation.'
