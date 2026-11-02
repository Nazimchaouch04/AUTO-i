<<<<<<< ours
# AUTO-i

Plateforme d'analyse du marché automobile avec estimation de prix.

## Installation

```bash
git clone https://github.com/Nazimchaouch04/AUTO-i.git
cd AUTO-i
```

Voir la branche `development` pour le code complet.
=======
# AUTO-P / AutoIntel - Contexte projet pour IA

Ce fichier est concu pour etre donne a ChatGPT, Claude ou un autre assistant IA afin de comprendre rapidement le projet, son architecture et les fichiers importants a lire avant de modifier le code.

## Resume rapide

AUTO-P, aussi appele AutoIntel dans le code, est une application web d'analyse du marche automobile. Elle permet notamment de consulter des annonces de vehicules, estimer des prix, gerer des alertes, afficher des statistiques, utiliser un assistant IA, acceder a une marketplace et proposer des elements de gamification.

Le projet contient deux applications principales:

- `backend/`: API Django + Django REST Framework.
- `frontend/`: interface React + Vite.

En developpement local:

- Frontend: `http://127.0.0.1:5173/`
- Backend API: `http://127.0.0.1:8000/`
- Admin Django: `http://127.0.0.1:8000/admin/`

## Stack technique

Backend:

- Python
- Django 4.2
- Django REST Framework
- JWT avec `djangorestframework-simplejwt`
- SQLite en developpement local
- PostgreSQL possible via configuration/deploiement
- Stripe pour les abonnements/paiements
- Celery/Redis prevus pour certaines taches
- Scikit-learn, pandas, numpy, joblib pour l'estimation/ML

Frontend:

- React 18
- Vite
- React Router
- Redux Toolkit
- Axios
- React Query
- Recharts
- Framer Motion
- Tailwind CSS
- Lucide React

## Architecture generale

```text
Navigateur
  |
  v
frontend/ React + Vite, port 5173
  |
  | Requetes HTTP vers /api/* avec JWT
  v
backend/ Django + DRF, port 8000
  |
  +-- apps Django metier
  +-- SQLite: backend/db.sqlite3 en dev
  +-- PostgreSQL possible selon configuration
```

Le frontend appelle directement le backend via `frontend/src/api/axiosClient.js`. La variable `VITE_API_URL` peut surcharger l'URL API; sinon la valeur par defaut est `http://localhost:8000`.

## Arborescence utile

```text
AUTO-P/
  backend/
    manage.py
    autointel/
      settings.py
      urls.py
      views.py
      wsgi.py
      asgi.py
    apps/
      users/
      annonces/
      vehicules/
      estimation/
      dashboard/
      alertes/
      subscriptions/
      gamification/
      ai_assistant/
      marketplace/
      notifications/
      rapports/
      scraping/
      admin_panel/
      core/
    db.sqlite3
    requirements.txt
    pytest.ini

  frontend/
    src/
      App.jsx
      main.jsx
      api/
      components/
      hooks/
      layouts/
      pages/
      store/
      styles/
    package.json
    vite.config.js

  docker-compose.yml
  start_servers.bat
  README.md
```

Les dossiers `.venv`, `.venv311`, `node_modules`, `dist`, `.vite`, `__pycache__`, `postgres_data` et les fichiers de logs sont des dependances, caches, bases locales ou sorties generees. Ne pas les traiter comme le code applicatif principal.

## Backend Django

### Fichiers d'entree

- `backend/manage.py`: commandes Django.
- `backend/autointel/settings.py`: configuration principale actuelle.
- `backend/autointel/urls.py`: routes globales de l'API.
- `backend/autointel/views.py`: vues simples comme la racine API et le healthcheck.
- `backend/requirements.txt`: dependances Python.

### Apps metier

- `apps.users`: utilisateurs, profils, inscription, authentification.
- `apps.annonces`: annonces automobiles, filtres, favoris, recherches, battles.
- `apps.vehicules`: catalogue vehicules, marques, modeles.
- `apps.estimation`: estimation de prix, logique ML.
- `apps.dashboard`: statistiques et indicateurs.
- `apps.alertes`: alertes de recherche et suivi du marche.
- `apps.subscriptions`: abonnements, plans, logique Stripe.
- `apps.gamification`: XP, niveaux, defis, boutique, classement.
- `apps.ai_assistant`: assistant IA, conversations, recommandations.
- `apps.marketplace`: marketplace, vendeurs, messages, reviews, logistique.
- `apps.notifications`: notifications, email, Telegram, WhatsApp.
- `apps.rapports`: generation et gestion de rapports.
- `apps.scraping`: collecte externe de donnees.
- `apps.admin_panel`: personnalisation/admin.
- `apps.core`: composants communs, permissions, pagination, middleware.

Une app Django suit en general ce schema:

```text
apps/<nom_app>/
  models.py
  serializers.py
  views.py
  urls.py
  admin.py
  migrations/
```

Certains modules ont aussi des fichiers alternatifs ou historiques comme `views_old.py`, `models_fixed.py`, `admin_old.py`, etc. Avant toute modification, verifier quel fichier est importe par les `urls.py`, `apps.py` et `settings.py`.

### Routes API globales

Les routes principales sont dans `backend/autointel/urls.py`:

- `/` et `/api/`: racine API.
- `/api/health/`: verification de disponibilite.
- `/admin/`: administration Django.
- `/api/auth/login/`: obtention des tokens JWT.
- `/api/auth/refresh/`: renouvellement du token JWT.
- `/api/auth/verify/`: verification du token JWT.
- `/api/auth/`: routes utilisateurs.
- `/api/annonces/`: annonces.
- `/api/vehicules/`: vehicules, marques, modeles.
- `/api/estimation/`: estimation de prix.
- `/api/dashboard/`: dashboard/statistiques.
- `/api/alertes/`: alertes.
- `/api/subscriptions/`: abonnements.
- `/api/gamification/`: gamification.
- `/api/ai/`: assistant IA.
- `/api/marketplace/`: marketplace.
- `/api/notifications/`: notifications.
- `/api/rapports/`: rapports.

### Authentification

Le backend utilise JWT via `rest_framework_simplejwt`.

Flux principal:

1. Le frontend envoie les identifiants a `/api/auth/login/`.
2. Le backend renvoie un `access` token et un `refresh` token.
3. Le frontend stocke les tokens dans `localStorage`.
4. `frontend/src/api/axiosClient.js` ajoute `Authorization: Bearer <token>` aux requetes.
5. En cas de `401`, le frontend tente `/api/auth/refresh/`.
6. Si le refresh echoue, les tokens sont supprimes et l'utilisateur est renvoye vers `/login`.

### Base de donnees

La configuration locale actuelle dans `backend/autointel/settings.py` utilise SQLite:

```text
backend/db.sqlite3
```

Le projet contient aussi des elements PostgreSQL (`docker-compose.yml`, `postgres_data`, scripts de migration), mais la configuration active doit toujours etre verifiee dans `settings.py` ou les fichiers `backend/autointel/settings/` avant de changer la base.

## Frontend React

### Fichiers d'entree

- `frontend/src/main.jsx`: point de montage React.
- `frontend/src/App.jsx`: routes React actives.
- `frontend/src/api/axiosClient.js`: client HTTP Axios et gestion JWT.
- `frontend/src/store/`: Redux store et slices.
- `frontend/src/layouts/`: layouts publics, auth et espace connecte.
- `frontend/src/pages/`: pages actuellement utilisees par le routeur principal.
- `frontend/vite.config.js`: configuration Vite et proxy `/api`.
- `frontend/package.json`: scripts et dependances frontend.

### Routes frontend actives

Les routes actives sont declarees dans `frontend/src/App.jsx`.

Routes publiques:

- `/`: landing page.
- `/login`: connexion.
- `/register`: inscription.

Routes protegees par `PrivateRoute`:

- `/dashboard`
- `/annonces`
- `/marketplace`
- `/estimation`
- `/alertes`
- `/profil`
- `/abonnement`
- `/classement`
- `/defis`
- `/boutique`
- `/battles`
- `/tournois`
- `/collection`
- `/season-pass`

Route inconnue:

- `*`: page 404.

Point important: `frontend/src/components/pages/` contient aussi des composants plus anciens ou alternatifs. Le routeur actuel charge surtout les fichiers de `frontend/src/pages/`. Avant de modifier une page, verifier l'import dans `App.jsx`.

## Commandes de lancement

### Lancement automatique

Depuis la racine:

```powershell
.\start_servers.bat
```

Ce script lance:

- Backend Django sur `http://127.0.0.1:8000`
- Frontend Vite sur `http://localhost:5173`

### Lancement manuel backend

Depuis la racine du projet:

```powershell
cd backend
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
```

Selon l'environnement local, il peut aussi exister `.venv311`.

### Lancement manuel frontend

Depuis la racine du projet:

```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

## Tests et verification

Backend:

```powershell
cd backend
..\.venv\Scripts\python.exe manage.py check
..\.venv\Scripts\python.exe manage.py test
```

Frontend:

```powershell
cd frontend
npm run build
npm run lint
```

Controle HTTP rapide apres lancement:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/api/health/ -UseBasicParsing
Invoke-WebRequest http://127.0.0.1:5173/ -UseBasicParsing
```

## Fichiers de documentation existants

Le depot contient plusieurs rapports Markdown historiques. Ils peuvent aider, mais le code actif reste la source de verite.

Fichiers utiles:

- `PROJECT_STRUCTURE_REPORT.md`: rapport de structure complet.
- `PROJET_RAPPORT.md`: resume court.
- `rapport.md`: rapport plus long.
- `BACKEND_IMPROVEMENTS_SUMMARY.md`: historique backend.
- `AI_ASSISTANT_DEVELOPMENT_REPORT.md`: contexte assistant IA.
- `MIGRATION_POSTGRESQL.md`: notes PostgreSQL.
- `deployment_guide.md`: notes de deploiement.

Attention: certains README ou rapports anciens contiennent des routes ou composants qui ne sont plus forcement ceux utilises par `frontend/src/App.jsx` et `backend/autointel/urls.py`.

## Points de vigilance pour une IA

Avant de modifier le projet:

1. Lire `backend/autointel/settings.py` pour connaitre la configuration active.
2. Lire `backend/autointel/urls.py` pour connaitre les routes API actives.
3. Lire `frontend/src/App.jsx` pour connaitre les pages vraiment utilisees.
4. Lire `frontend/src/api/axiosClient.js` pour comprendre les appels API et JWT.
5. Verifier si le fichier a modifier est importe quelque part.
6. Eviter de modifier les fichiers `*_old.py`, `*_broken.py`, `*_fixed.py` sans verifier leur usage.
7. Ne pas exposer les secrets, tokens, cles Stripe, base locale ou identifiants admin.
8. Ne pas supprimer `db.sqlite3` ou `postgres_data` sans demande explicite.
9. Ne pas faire de refonte globale si la demande concerne une page, une route ou un bug precis.
10. Apres modification, lancer au minimum un check backend ou un build frontend selon la zone touchee.

## Parcours de lecture conseille pour ChatGPT/Claude

Pour comprendre rapidement le projet, lire dans cet ordre:

1. `README.md`
2. `backend/autointel/settings.py`
3. `backend/autointel/urls.py`
4. `frontend/src/App.jsx`
5. `frontend/src/api/axiosClient.js`
6. Le dossier de l'app Django concernee dans `backend/apps/`
7. La page React concernee dans `frontend/src/pages/`
8. Les serializers/views/models associes cote backend

Chemin mental principal:

```text
Page React
  -> axiosClient
  -> endpoint /api/*
  -> urls.py de l'app Django
  -> view ou ViewSet
  -> serializer
  -> model
  -> base SQLite/PostgreSQL
```

## Resume pour une IA en une phrase

AUTO-P / AutoIntel est une application full-stack Django REST + React/Vite pour l'analyse du marche automobile, avec annonces, estimation de prix, dashboard, alertes, authentification JWT, marketplace, abonnements, gamification, assistant IA et rapports; les sources de verite sont `backend/autointel/urls.py`, `backend/autointel/settings.py`, `frontend/src/App.jsx` et `frontend/src/api/axiosClient.js`.
>>>>>>> theirs





