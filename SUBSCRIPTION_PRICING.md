# Configuration des Prix d'Abonnement - AUTO-P

## 📊 Plans Actuels

### Plan GRATUIT
- **Prix**: 0€/mois
- **Estimations**: 5/mois
- **Alertes**: 2
- **Export CSV**: Non
- **Accès API**: Non
- **Idéal**: Découverte de la plateforme

### Plan PRO
- **Prix**: 19.99€/mois
- **Estimations**: 50/mois
- **Alertes**: 20
- **Export CSV**: Oui
- **Accès API**: Non
- **Idéal**: Utilisateurs réguliers, particuliers

### Plan BUSINESS
- **Prix**: 49.99€/mois
- **Estimations**: 999/mois (illimité)
- **Alertes**: 100
- **Export CSV**: Oui
- **Accès API**: Oui
- **Idéal**: Professionnels, concessionnaires, flottes

---

## 🔧 Comment Modifier les Prix

### Option 1: Via Script (Recommandé)

```bash
cd backend
python setup_subscription_plans.py
```

Éditez le fichier `setup_subscription_plans.py` pour changer les prix:

```python
PLANS_CONFIG = [
    {
        'nom': 'free',
        'prix_mensuel': 0,  # ← Modifier ici
        'estimations_par_mois': 5,
        # ...
    },
    {
        'nom': 'pro',
        'prix_mensuel': 29.99,  # ← Ex: changer de 19.99 à 29.99
        # ...
    },
]
```

### Option 2: Via Admin Django

1. Allez sur http://127.0.0.1:8000/admin/
2. Connectez-vous (admin@autointel.com / AutoIntel2024!)
3. Allez dans "Subscriptions" > "Plans"
4. Modifiez les prix directement

### Option 3: Via Django Shell

```bash
cd backend
python manage.py shell
```

```python
from apps.subscriptions.models import Plan

# Modifier le plan Pro
pro = Plan.objects.get(nom='pro')
pro.prix_mensuel = 29.99
pro.save()

# Modifier le plan Business
business = Plan.objects.get(nom='business')
business.prix_mensuel = 79.99
business.save()
```

---

## 💰 Configuration Stripe

Pour que les paiements fonctionnent, vous devez configurer Stripe:

### 1. Créer les produits dans Stripe

Allez sur https://dashboard.stripe.com/products et créez:

**Produit: AutoIntel Free**
- Prix: 0€
- Facturation: Mensuelle

**Produit: AutoIntel Pro**
- Prix: 19.99€ (ou votre prix)
- Facturation: Mensuelle

**Produit: AutoIntel Business**
- Prix: 49.99€ (ou votre prix)
- Facturation: Mensuelle

### 2. Configurer les Webhooks

Dans Stripe Dashboard > Developers > Webhooks:
- **URL**: `https://votre-backend.com/api/subscriptions/webhook/`
- **Événements**:
  - `checkout.session.completed`
  - `customer.subscription.created`
  - `customer.subscription.updated`
  - `customer.subscription.deleted`
  - `invoice.payment_succeeded`
  - `invoice.payment_failed`

### 3. Ajouter les clés Stripe

Dans `backend/.env`:
```
STRIPE_PUBLIC_KEY=pk_live_votre_clé_publique
STRIPE_SECRET_KEY=sk_live_votre_clé_secrète
STRIPE_WEBHOOK_SECRET=whsec_votre_webhook_secret
```

---

## 📈 Stratégie de Prix Recommandée

### Marché Français/Européen

| Plan | Prix Actuel | Prix Suggéré | Justification |
|------|-------------|--------------|---------------|
| Free | 0€ | 0€ | Toujours gratuit pour attirer |
| Pro | 19.99€ | 9.99€-14.99€ | Plus compétitif vs LeBonCoin |
| Business | 49.99€ | 29.99€-39.99€ | Abordable pour PME |

### Marché International

| Plan | Prix EUR | Prix USD | Prix GBP |
|------|----------|----------|---------|
| Free | 0€ | $0 | £0 |
| Pro | 9.99€ | $12.99 | £8.99 |
| Business | 29.99€ | $39.99 | £24.99 |

---

## 🎯 Fonctionnalités par Plan

### Gratuit (Free Tier)
- ✅ 5 estimations/mois
- ✅ 2 alertes
- ❌ Pas d'export CSV
- ❌ Pas d'accès API
- ❌ Support standard

### Pro
- ✅ 50 estimations/mois
- ✅ 20 alertes
- ✅ Export CSV
- ❌ Pas d'accès API
- ✅ Support prioritaire (email)

### Business
- ✅ Estimations illimitées
- ✅ 100 alertes
- ✅ Export CSV
- ✅ Accès API complet
- ✅ Support dédié (téléphone + email)
- ✅ Formation incluse

---

## 💡 Conseils de Tarification

1. **Psychologie des prix**
   - 9.99€ semble moins cher que 10€
   - 19.99€ est un standard pour les SaaS
   - Évitez les prix ronds (20€, 50€)

2. **Essai gratuit**
   - Proposez 14-30 jours gratuits sur Pro
   - Conversion attendue: 5-10%

3. **Réduction annuelle**
   - -20% pour paiement annuel
   - Ex: Pro = 9.99€/mois ou 95.90€/an (économie 24€)

4. **Promotions**
   - -50% pour les 100 premiers clients
   - Offres spéciales pour les étudiants

---

## 🔄 Mise à jour des Prix Existant

Si vous changez les prix:

1. **Nouveaux abonnés**: Paieront le nouveau prix
2. **Anciens abonnés**: Gardent leur prix (grandfathering)
3. **Communication**: Informez 30 jours avant
4. **Légal**: Respectez les CGU existantes

---

## 📊 Suivi des Revenus

### KPIs à surveiller

- **MRR** (Monthly Recurring Revenue)
- **ARR** (Annual Recurring Revenue)
- **Churn rate** (taux d'annulation)
- **LTV** (Lifetime Value)
- **CAC** (Customer Acquisition Cost)

### Formules

```
MRR = (Nombre Pro × Prix Pro) + (Nombre Business × Prix Business)
ARR = MRR × 12
Churn Rate = (Annulations / Total Abonnés) × 100
LTV = (Prix Mensuel × Durée Moyenne Abonnement)
```

---

## ✅ Checklist Production

- [ ] Prix configurés dans la base de données
- [ ] Produits créés dans Stripe
- [ ] Webhooks configurés
- [ ] Clés Stripe ajoutées en production
- [ ] Test de paiement complet
- [ ] Test d'annulation
- [ ] Test de renouvellement
- [ ] CGU mises à jour avec les nouveaux prix

---

**Document mis à jour**: 2 Novembre 2026
