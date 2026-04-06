# 🚀 AutoIntel - Guide de Déploiement Complet

Suivez ces étapes pour mettre votre application AutoIntel en production.

## 📦 ÉTAPE 1 : Préparez le Code
Initialisez git et poussez votre code vers un nouveau dépôt GitHub.
```bash
git init
git add .
git commit -m "feat: AutoIntel v1.0 - Production ready"
git branch -M main
git remote add origin https://github.com/VOTRE_USER/autointel.git
git push -u origin main
```

---

## ☁️ ÉTAPE 2 : Déployez le Backend (Railway)
1.  **Connectez-vous à Railway** : Allez sur [railway.app](https://railway.app) et connectez votre compte GitHub.
2.  **Nouveau Projet** : "New Project" -> "Deploy from GitHub repo" -> Sélectionnez `autointel`.
3.  **Root Directory** : Choisissez le dossier `backend`.
4.  **Ajoutez la Base de Données** : "New Service" -> "Database" -> "PostgreSQL".
5.  **Variables d'Environnement** :
    Dans votre service backend Railway, configurez :
    - `SECRET_KEY` : Générez avec `python -c "import secrets; print(secrets.token_hex(32))"`.
    - `DEBUG` : `False`
    - `ALLOWED_HOSTS` : `autointel-backend.up.railway.app`
    - `CORS_ORIGINS` : `https://autointel.vercel.app`
    - `STRIPE_SECRET_KEY` : Votre clé secrète Stripe.
    - `STRIPE_PUBLIC_KEY` : Votre clé publique Stripe.
    - `STRIPE_WEBHOOK_SECRET` : Votre secret de webhook Stripe (voir étape 4).
    - `FRONTEND_URL` : `https://autointel.vercel.app`
    *(Note: DATABASE_URL est injecté automatiquement par Railway)*
6.  **Déploiement** : Railway construira le projet via Nixpacks et lancera les migrations.

---

## ⚡ ÉTAPE 3 : Déployez le Frontend (Vercel)
1.  **Connectez-vous à Vercel** : Allez sur [vercel.com](https://vercel.com) et connectez votre GitHub.
2.  **Nouveau Projet** : Importez votre dépôt `autointel`.
3.  **Configuration du Build** :
    - **Framework Preset** : `Vite`
    - **Root Directory** : `frontend`
    - **Build Command** : `npm run build`
    - **Output Directory** : `dist`
4.  **Variables d'Environnement** :
    - `VITE_API_URL` : `https://autointel-backend.up.railway.app`
5.  **Déploiement** : Attendez que le build soit terminé ✅.

---

## 💳 ÉTAPE 4 : Configurez les Webhooks Stripe
1.  Dans le dashboard Stripe : **Developers** -> **Webhooks** -> **Add endpoint**.
2.  **URL** : `https://autointel-backend.up.railway.app/api/subscriptions/webhook/`.
3.  **Événements à écouter** :
    - `checkout.session.completed`
    - `customer.subscription.deleted`
    - `customer.subscription.updated`
    - `invoice.payment_failed`
4.  Copiez le **Webhook Secret** et mettez-le dans `STRIPE_WEBHOOK_SECRET` sur Railway.

---

## ✅ ÉTAPE 5 : Test Final en Production
- Vérifiez que [autointel.vercel.app](https://autointel.vercel.app) se charge.
- Testez la connexion et l'estimation.
- Vérifiez l'administration Django : `https://autointel-backend.up.railway.app/admin/`.

---

## 📊 Monitoring
 रेलवे (Railway) et Vercel fournissent des logs et des métriques intégrés. Pour le suivi des erreurs backend, vous pouvez ajouter [Sentry](https://sentry.io).
