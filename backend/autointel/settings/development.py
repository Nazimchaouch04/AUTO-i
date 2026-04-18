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

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Retirer WhiteNoise du MIDDLEWARE en dev (non installe / non requis)
MIDDLEWARE = [m for m in MIDDLEWARE if 'whitenoise' not in m]

# Fichiers statiques servis directement par Django en dev
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
