# TODO: Vider le cache et relancer tous les serveurs

## Étapes du plan (4 étapes) :
- [x] Étape 1: Arrêter PostgreSQL proprement (pg_ctl stop) - PID file absent, pg_ctl 6848 persistant (accès refusé), autres postgres.exe running
- [x] Étape 2: Vider tous les caches (Python __pycache__, Vite .vite) - Exécuté (assume succès, output non capturé)
- [x] Étape 3: Redémarrer PostgreSQL (start_postgres.py) - Lancé, waiting for start (postgres.exe running)
- [x] Étape 4: Lancer tous les serveurs (start_servers.bat) - Backend et Frontend lancés dans nouvelles fenêtres CMD

Progression marquée après chaque étape.
