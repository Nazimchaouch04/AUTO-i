# Migration SQLite vers PostgreSQL - AutoIntel

## Pourquoi PostgreSQL ?

PostgreSQL est une base de données beaucoup plus robuste que SQLite pour la production :

- **Performance** : Meilleures performances pour les requêtes complexes
- **Concurrence** : Gère mieux les accès simultanés
- **Scalabilité** : Supporte des volumes de données beaucoup plus importants
- **Features** : Fonctionnalités avancées (JSON, indexes, etc.)
- **Production** : Standard pour les applications Django en production

## Étapes de Migration

### 1. Installation PostgreSQL

#### Option A : Automatique (Recommandé)
```bash
# Exécuter le script d'installation
./install_postgres_windows.bat
```

#### Option B : Manuel
1. Télécharger PostgreSQL depuis https://www.postgresql.org/download/windows/
2. Installer avec les options par défaut
3. Noter le mot de passe (par défaut: `postgres123`)

### 2. Configuration Django

Les settings sont déjà configurés pour PostgreSQL dans `backend/autointel/settings.py` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='autointel_db'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='postgres123'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

### 3. Variables d'Environnement

Créez un fichier `.env` dans `backend/` :

```bash
# Configuration PostgreSQL
DB_NAME=autointel_db
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=localhost
DB_PORT=5432
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/autointel_db
```

### 4. Migration des Données

#### Étape 4.1 : Exporter les données SQLite
```bash
cd backend
python migrate_to_postgres.py
```

Ce script va :
- Exporter toutes les tables SQLite vers des fichiers JSON
- Créer les tables PostgreSQL avec `python manage.py migrate`
- Importer les données dans PostgreSQL

#### Étape 4.2 : Vérification
```bash
# Vérifier que les données sont bien là
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.count()
>>> from apps.annonces.models import Annonce
>>> Annonce.objects.count()
```

### 5. Test Final

```bash
# Démarrer le serveur avec PostgreSQL
python manage.py runserver

# Tester l'API
curl http://localhost:8000/api/health/
```

## Fichiers Créés

- `backend/setup_postgresql.py` : Script de vérification PostgreSQL
- `backend/migrate_to_postgres.py` : Script de migration des données
- `install_postgres_windows.bat` : Script d'installation automatique
- `MIGRATION_POSTGRESQL.md` : Ce guide

## Dépannage

### Problèmes Communs

1. **PostgreSQL ne démarre pas**
   ```bash
   # Démarrer le service manuellement
   net start postgresql-x64-15
   ```

2. **Erreur de connexion**
   - Vérifiez que PostgreSQL est en cours d'exécution
   - Vérifiez les identifiants dans `.env`
   - Vérifiez que la base de données `autointel_db` existe

3. **Migration échoue**
   - Sauvegardez votre `db.sqlite3`
   - Recréez la base de données PostgreSQL
   - Relancez la migration

### Commandes Utiles

```bash
# Se connecter à PostgreSQL
psql -U postgres -d autointel_db

# Lister les tables
\dt

# Vérifier les données
SELECT COUNT(*) FROM auth_user;
SELECT COUNT(*) FROM annonces_annonce;

# Recréer la base de données
DROP DATABASE autointel_db;
CREATE DATABASE autointel_db;
```

## Avantages Après Migration

- **Performance** : Requêtes plus rapides
- **Stabilité** : Moins de corruption de données
- **Scalabilité** : Supporte plus d'utilisateurs simultanés
- **Features** : Indexation avancée, requêtes JSON
- **Production** : Prêt pour le déploiement

## Backup et Recovery

```bash
# Backup PostgreSQL
pg_dump -U postgres autointel_db > backup.sql

# Restore PostgreSQL
psql -U postgres autointel_db < backup.sql
```

---

**Note** : Après la migration, vous pouvez supprimer le fichier `db.sqlite3` et les dossiers d'export JSON.
