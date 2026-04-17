from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'autointel-dev',
    }
}

# Session en mémoire en dev (pas de Redis requis)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Désactiver WhiteNoise en dev (fichiers servis directement)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
