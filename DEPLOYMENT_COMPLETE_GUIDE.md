# Guide de Déploiement Production - AUTO-P

## 📋 Prérequis

- Compte GitHub (gratuit)
- Compte Railway (https://railway.app)
- Compte Vercel (https://vercel.com)
- Compte Stripe (https://stripe.com)
- Nom de domaine (optionnel, recommandé)

---

## ÉTAPE 1: Préparation du Code

### 1.1 Nettoyer les fichiers

```bash
cd AUTO-P
python cleanup_before_deploy.py
```

### 1.2 Committer les changements

```bash
git add .
git commit -m "Ready for production deployment"
git push origin development
```

---

## ÉTAPE 2: Déploiement Backend (Railway)

### 2.1 Créer un projet Railway

1. Allez sur https://railway.app
2. Connectez-vous avec GitHub
3. Cliquez sur **New Project**
4. Sélectionnez **Deploy from GitHub repo**
5. Choisissez votre repo AUTO-P

### 2.2 Configurer le backend

Dans Railway:
1. Cliquez sur **New Service**
2. Sélectionnez **Dockerfile**
3. Railway détectera automatiquement le backend

### 2.3 Ajouter PostgreSQL

1. Cliquez sur **New Service**
2. Sélectionnez **PostgreSQL**
3. Railway créera une base de données

### 2.4 Configurer les variables d'environnement

Dans les settings du service backend, ajoutez:

```bash
# Django
DEBUG=False
SECRET_KEY=<générer avec: python -c "import secrets; print(secrets.token_urlsafe(50))">
ALLOWED_HOSTS=votre-backend.railway.app,www.votre-domaine.com

# Database (Railway injecte DATABASE_URL automatiquement)
DATABASE_URL=${{RAILWAY_PRIVATE_DOMAIN}}

# CORS
CORS_ORIGINS=https://votre-frontend.vercel.app,https://www.votre-domaine.com
FRONTEND_URL=https://votre-frontend.vercel.app

# Stripe
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Autres
DJANGO_SETTINGS_MODULE=autointel.settings
```

### 2.5 Lancer les migrations

Dans le service backend, ajoutez une commande de build:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 2.6 Obtenir l'URL du backend

Railway vous donnera une URL comme:
`https://auto-p-backend-production.up.railway.app`

Copiez cette URL pour l'étape suivante.

---

## ÉTAPE 3: Déploiement Frontend (Vercel)

### 3.1 Installer Vercel CLI

```bash
npm install -g vercel
```

### 3.2 Déployer le frontend

```bash
cd frontend
vercel --prod
```

Suivez les instructions:
1. Connectez-vous avec votre compte Vercel
2. Sélectionnez le projet
3. Vercel détectera automatiquement Vite

### 3.3 Configurer les variables d'environnement

Dans Vercel > Settings > Environment Variables:

```bash
VITE_API_URL=https://votre-backend.railway.app
```

### 3.4 Obtenir l'URL du frontend

Vercel vous donnera une URL comme:
`https://auto-p-frontend.vercel.app`

---

## ÉTAPE 4: Configuration Domaine

### 4.1 Acheter un domaine

Achetez un domaine chez:
- Namecheap
- GoDaddy
- Google Domains

### 4.2 Configurer le domaine Vercel

1. Allez dans Vercel > Settings > Domains
2. Ajoutez votre domaine (ex: autointel.com)
3. Vercel vous donnera les DNS à configurer

### 4.3 Configurer le domaine Railway

1. Allez dans Railway > Settings > Domains
2. Ajoutez api.autointel.com
3. Configurez les DNS

### 4.4 Mettre à jour les variables d'environnement

Mettez à jour ALLOWED_HOSTS et CORS_ORIGINS avec votre vrai domaine.

---

## ÉTAPE 5: Configuration Stripe Production

### 5.1 Passer en mode Live

Dans Stripe Dashboard:
1. Cliquez sur **Test mode** pour le désactiver
2. Passez en **Live mode**

### 5.2 Obtenir les clés live

1. Allez dans **Developers** > **API keys**
2. Copiez:
   - **Publishable key**: `pk_live_...`
   - **Secret key**: `sk_live_...`

### 5.3 Créer les produits live

Créez les mêmes produits qu'en test mais avec les vrais prix:
- AutoIntel Free: 0€
- AutoIntel Pro: 19.99€
- AutoIntel Business: 49.99€

### 5.4 Configurer les webhooks

1. Créez un webhook avec l'URL de production
2. Sélectionnez les mêmes événements
3. Copiez le webhook signing secret

### 5.5 Mettre à jour les variables d'environnement

Mettez à jour STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY et STRIPE_WEBHOOK_SECRET avec les clés live.

---

## ÉTAPE 6: Tests de Production

### 6.1 Tester le backend

```bash
curl https://votre-backend.railway.app/api/health/
```

Devrait retourner:
```json
{"status":"healthy","db":"OK","endpoints_total":14,"endpoints_ok":14}
```

### 6.2 Tester le frontend

Allez sur https://votre-frontend.vercel.app et vérifiez:
- Page d'accueil s'affiche
- Login fonctionne
- Estimation fonctionne

### 6.3 Tester le paiement

1. Créez un compte utilisateur
2. Essayez de souscrire à un abonnement
3. Utilisez une carte de test Stripe:
   - Numéro: 4242 4242 4242 4242
   - Expiration: 12/34
   - CVC: 123

### 6.4 Vérifier les logs

- Railway: Logs du service backend
- Vercel: Logs du frontend
- Stripe: Dashboard > Events

---

## ÉTAPE 7: Monitoring et Maintenance

### 7.1 Configurer les alertes

**Railway**:
- Configurez les alertes de CPU, mémoire, erreurs

**Vercel**:
- Activez les alertes d'erreurs

**Stripe**:
- Configurez les alertes de paiement échoué

### 7.1 Backups

Railway effectue des backups automatiques de PostgreSQL. Vérifiez:
- Fréquence des backups (quotidien recommandé)
- Rétention (30 jours minimum)

### 7.2 Mises à jour

Pour mettre à jour le code:

```bash
git pull
# Railway et Vercel déploieront automatiquement
```

---

## 📊 Coûts Mensuels Estimés

| Service | Plan | Coût |
|---------|------|------|
| Railway (Backend + DB) | Hobby | $5-20 |
| Vercel (Frontend) | Pro | $20 |
| Domaine | - | $1-2 |
| Stripe | - | 2.9% + $0.30/transaction |
| **Total** | | **$26-42/mois** |

---

## 🔧 Dépannage

### Backend ne démarre pas

Vérifiez les logs Railway:
- SECRET_KEY est défini?
- DATABASE_URL est correct?
- Migrations appliquées?

### Frontend ne se connecte pas

Vérifiez:
- VITE_API_URL est correct?
- CORS_ORIGINS inclut l'URL frontend?
- Backend est accessible?

### Paiement échoue

Vérifiez:
- Clés Stripe sont en mode live?
- Webhook est configuré?
- URL webhook est accessible?

---

## ✅ Checklist Finale

- [ ] Code nettoyé et commité
- [ ] Backend déployé sur Railway
- [ ] PostgreSQL configuré
- [ ] Frontend déployé sur Vercel
- [ ] Domaine configuré
- [ ] Stripe en mode live
- [ ] Webhooks configurés
- [ ] Tests de production passés
- [ ] Monitoring configuré
- [ ] Backups vérifiés

---

## 📞 Support

En cas de problème:
- Documentation Railway: https://docs.railway.app
- Documentation Vercel: https://vercel.com/docs
- Documentation Stripe: https://stripe.com/docs

---

**Guide créé**: 2 Novembre 2026
