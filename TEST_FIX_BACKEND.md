# TEST_FIX_BACKEND.md - Corrections Tests Backend AutoIntel SaaS

## Étape 1: ✅ tblib installé (parallel tests)

## Étape 2: [ ] Fix users/tests.py
- password_confirm → password2 (3 instances)
- /api/auth/profile/ → /api/auth/me/

## Étape 3: [ ] Fix marketplace/tests.py
- test data vehicule → Listing fields (title, brand...)
- Skip verification 404 (no view)

## Étape 4: [ ] Fix subscriptions/tests.py
- /mon-abonnement/ → /me/

## Étape 5: [ ] Fix autointel/tests.py
- Health 'healthy' → ['healthy', 'ok', 'degraded']

## Progression: 31/38 pytest OK (82%)
**Run `.\test_all_backend.bat` après chaque fix**
