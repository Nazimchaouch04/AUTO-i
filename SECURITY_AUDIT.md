# Audit de Sécurité - AUTO-P / AutoIntel

## 🔍 Analyse de Sécurité Actuelle

### ✅ Mesures de Sécurité en Place

1. **Authentification**
   - ✅ JWT tokens (SimpleJWT)
   - ✅ Refresh tokens rotation
   - ✅ Password validators (Django default)
   - ✅ Token expiration configurable

2. **Autorisation**
   - ✅ Permission classes (IsAuthenticatedOrReadOnly)
   - ✅ Protected routes via PrivateRoute (frontend)
   - ✅ Admin panel protection

3. **CORS**
   - ✅ django-cors-headers configuré
   - ✅ Origins whitelist

4. **Production Security** (partiel)
   - ✅ SECURE_BROWSER_XSS_FILTER (en prod)
   - ✅ SECURE_CONTENT_TYPE_NOSNIFF (en prod)
   - ✅ X_FRAME_OPTIONS (en prod)
   - ✅ SESSION_COOKIE_SECURE (en prod)
   - ✅ CSRF_COOKIE_SECURE (en prod)

### ⚠️ Vulnérabilités et Risques Identifiés

#### Critique (Doit être corrigé)

1. **SECRET_KEY par défaut**
   - **Problème**: `django-insecure-autointel-dev-key-change-in-prod`
   - **Risque**: Attaques sur les sessions, forgery
   - **Solution**: Générer une clé forte en production

2. **DEBUG=True en développement**
   - **Problème**: Informations sensibles exposées en cas d'erreur
   - **Risque**: Fuite de données, stack traces
   - **Solution**: Toujours DEBUG=False en production

3. **ALLOWED_HOSTS = ['*']**
   - **Problème**: Accepte tous les hôtes
   - **Risque**: Host header attacks
   - **Solution**: Lister les domaines autorisés

4. **Pas de rate limiting**
   - **Problème**: Pas de limite sur les requêtes API
   - **Risque**: DDoS, brute force attacks
   - **Solution**: Implémenter django-ratelimit

#### Haut (Devrait être corrigé)

5. **Pas de HTTPS forcé**
   - **Problème**: HTTP autorisé
   - **Risque**: Interception de données (MITM)
   - **Solution**: HSTS, SSL redirect

6. **Tokens JWT trop longs**
   - **Problème**: Access token = 1h, Refresh = 7 jours
   - **Risque**: Tokens volés utilisables longtemps
   - **Solution**: Réduire à 15min access, 1 jour refresh

7. **Pas de logging des authentifications**
   - **Problème**: Impossible de détecter les attaques
   - **Risque**: Intrusions non détectées
   - **Solution**: Logging des login/échecs

8. **Pas de validation des inputs**
   - **Problème**: Possibilité d'injection
   - **Risque**: XSS, SQL injection
   - **Solution**: Validators stricts

#### Moyen (Pourrait être amélioré)

9. **Pas de 2FA**
   - **Problème**: Mot de passe seul
   - **Risque**: Compromission par phishing
   - **Solution**: TOTP optionnel

10. **Pas de password policy**
    - **Problème**: Mot de passe minimum 6 caractères
    - **Risque**: Mots de passe faibles
    - **Solution**: Complexité requise

11. **Pas de CSRF protection sur API**
    - **Problème**: API stateless
    - **Risque**: CSRF sur endpoints sensibles
    - **Solution**: Double submit cookie ou SameSite

12. **Pas de encryption des données sensibles**
    - **Problème**: Données en clair dans DB
    - **Risque**: Exposition si DB compromise
    - **Solution**: Field encryption (django-fernet-fields)

---

## 🔐 Plan d'Amélioration de Sécurité

### Phase 1: Critique (Immédiat)

#### 1.1 Configuration Production Sécurisée

Créer `backend/autointel/settings_production.py`:

```python
from .settings import *

# Sécurité de base
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# HTTPS obligatoire
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies sécurisés
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# Headers de sécurité
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# CORS strict
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
CORS_ALLOW_CREDENTIALS = True
```

#### 1.2 JWT Tokens Sécurisés

Modifier `backend/autointel/settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # 15 min au lieu de 1h
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # 1 jour au lieu de 7 jours
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}
```

#### 1.3 Rate Limiting

Installer django-ratelimit:

```bash
pip install django-ratelimit
```

Ajouter dans `settings.py`:

```python
INSTALLED_APPS += ['django_ratelimit']

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',      # 100 requêtes/heure pour anonymes
        'user': '1000/hour',     # 1000 requêtes/heure pour authentifiés
        'login': '5/hour',       # 5 tentatives de login/heure
        'estimation': '20/hour', # 20 estimations/heure
    }
}
```

### Phase 2: Haut (Court terme)

#### 2.1 Password Policy

Installer django-password-validators:

```bash
pip install django-password-validators
```

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'django_password_validators.complexity.MinimumComplexityValidator',
        'OPTIONS': {
            'min_digits': 1,
            'min_upper': 1,
            'min_lower': 1,
            'min_special': 1,
        }
    }
]
```

#### 2.2 Logging Sécurité

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'security_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['security_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

#### 2.3 Input Validation

Ajouter des validators dans les serializers:

```python
from rest_framework import serializers

class EstimationSerializer(serializers.Serializer):
    marque = serializers.CharField(max_length=50)
    modele = serializers.CharField(max_length=50)
    annee = serializers.IntegerField(min_value=1990, max_value=2025)
    kilometrage = serializers.IntegerField(min_value=0, max_value=1000000)
    
    def validate_marque(self, value):
        # Sanitize input
        allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZéèêëâàäùüûôöîïç- ')
        if not all(c in allowed_chars for c in value):
            raise serializers.ValidationError("Caractères invalides")
        return value.strip()
```

### Phase 3: Moyen (Moyen terme)

#### 3.1 2FA Optionnel

Installer django-otp:

```bash
pip install django-otp qrcode
```

#### 3.2 Encryption des Données

Installer django-fernet-fields:

```bash
pip install django-fernet-fields
```

```python
from django.db import models
from fernet_fields import EncryptedCharField

class UserProfile(models.Model):
    # Champs sensibles encryptés
    phone_number = EncryptedCharField(max_length=20, blank=True)
    address = EncryptedCharField(max_length=255, blank=True)
```

#### 3.3 Security Headers Middleware

Créer `backend/apps/core/middleware.py`:

```python
class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['Content-Security-Policy'] = "default-src 'self'"
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        return response
```

---

## 🛡️ Checklist de Sécurité Production

### Avant Déploiement

- [ ] SECRET_KEY généré et stocké dans .env
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS configuré
- [ ] HTTPS activé (SSL certificate)
- [ ] HSTS activé
- [ ] Cookies sécurisés (Secure, HttpOnly, SameSite)
- [ ] JWT tokens réduits (15min access, 1j refresh)
- [ ] Rate limiting activé
- [ ] CORS restreint aux domaines autorisés
- [ ] Password policy renforcée (12+ caractères, complexité)
- [ ] Logging sécurité activé
- [ ] Input validation sur tous les endpoints
- [ ] Admin protégé (2FA optionnel)
- [ ] Base de données backup chiffré
- [ ] Fichiers statiques servis via CDN
- [ ] Media files upload validés et scannés

### Monitoring Sécurité

- [ ] Logs d'authentification surveillés
- [ ] Alertes sur tentatives de brute force
- [ ] Surveillance des requêtes anormales
- [ ] Scans de vulnérabilités réguliers
- [ ] Mises à jour de sécurité appliquées

---

## 📊 Outils de Sécurité Recommandés

### Backend
- **django-ratelimit**: Rate limiting
- **django-security**: Headers de sécurité
- **django-password-validators**: Password policy
- **django-otp**: 2FA
- **django-fernet-fields**: Encryption
- **django-auditlog**: Audit trail

### Frontend
- **helmet**: Security headers
- **dompurify**: XSS prevention
- **csrf-token**: CSRF protection
- **secure-ls**: LocalStorage encryption

### Infrastructure
- **Sentry**: Error tracking
- **Cloudflare**: DDoS protection, WAF
- **Let's Encrypt**: SSL certificates
- **Fail2Ban**: Brute force protection

---

## 🚨 Procédure en Cas d'Incident

### 1. Détection
- Alertes monitoring
- Logs anormaux
- Rapports utilisateurs

### 2. Containment
- Isoler les systèmes affectés
- Désactiver les comptes compromis
- Bloquer les IP malveillantes

### 3. Investigation
- Analyser les logs
- Identifier la source
- Évaluer l'impact

### 4. Recovery
- Restaurer les backups
- Appliquer les patchs
- Renforcer la sécurité

### 5. Communication
- Informer les utilisateurs
- Transparence sur l'incident
- Mesures prises

---

## 📚 Ressources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [REST Framework Security](https://www.django-rest-framework.org/api-guide/throttling/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)

---

**Audit réalisé**: 2 Novembre 2026
**Statut**: À implémenter
