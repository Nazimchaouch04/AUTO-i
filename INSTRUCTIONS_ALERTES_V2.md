# AUTOINTEL ALERTES V2 - WHATSAPP & TELEGRAM
## ✅ Module V2 Terminé

Le système d'alertes multi-canaux est maintenant entièrement intégré à AutoIntel !

### 🚀 Fonctionnalités implémentées

#### Backend
- ✅ **App `notifications`** avec modèles CanalNotification et NotificationHistory
- ✅ **Service Telegram** complet avec Bot API et formatting
- ✅ **Service WhatsApp** via Twilio avec validation et formatting  
- ✅ **Tasks Celery** pour envoi automatique des alertes
- ✅ **Endpoints REST** pour gestion complète des canaux
- ✅ **Système de vérification** des canaux (test messages)

#### Frontend
- ✅ **Section Notifications** dans AlertesPage.jsx avec onglets
- ✅ **Interface Telegram** : connexion, vérification, gestion
- ✅ **Interface WhatsApp** : configuration, test, gestion
- ✅ **Guide intégré** pour aider les utilisateurs
- ✅ **Statuts temps réel** des services configurés
- ✅ **Design responsive** et animations modernes

### 🔧 Configuration requise

1. **Variables d'environnement** (ajouter dans `backend/.env`) :
```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=1234567890:ABCDEF...

# Twilio WhatsApp  
TWILIO_ACCOUNT_SID=ACxxx
TWILIO_AUTH_TOKEN=xxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

2. **Dépendances installées** :
```bash
# Backend
pip install twilio  # déjà installé
```

3. **Base de données** :
```bash
python manage.py migrate  # déjà fait
```

### 🎯 Utilisation

#### Pour les utilisateurs

1. **Créer le bot Telegram** :
   - Suivez le guide `GUIDE_TELEGRAM_BOT.md`
   - Obtenez votre Chat ID
   - Connectez-le dans AutoIntel

2. **Configurer WhatsApp** :
   - Créez un compte Twilio (gratuit pour les tests)
   - Ajoutez votre numéro dans AutoIntel
   - Envoyez un message test

3. **Gérer les canaux** :
   - Allez dans "Alertes" → "Notifications"
   - Activez/désactivez les canaux selon vos préférences
   - Vérifiez les statuts en temps réel

#### Fonctionnalités
- **Alertes instantanées** : Temps réel sur Telegram et WhatsApp
- **Messages formatés** : Informations complètes avec prix, km, localisation
- **Gestion multi-canaux** : Combinez email, Telegram, WhatsApp
- **Historique complet** : Suivi de toutes les notifications envoyées
- **Vérification automatique** : Test de connexion avant activation

### 🔄 Intégration avec les alertes existantes

Le système s'intègre parfaitement aux alertes AutoIntel existantes :

1. **Créez vos alertes** comme d'habitude (marque, prix, km, etc.)
2. **Configurez vos canaux** de notification (Telegram, WhatsApp)
3. **Recevez instantanément** les nouvelles annonces correspondantes

Les alertes sont envoyées automatiquement toutes les 6 heures pour les nouvelles annonces correspondantes.

### 📱 Exemples de notifications reçues

**Telegram :**
```
🚗 NOUVELLE BONNE AFFAIRE !

🔥 15% SOUS LE MARCHÉ
BMW Série 3 2019
💰 Prix : 22 000 €
📍 Alger, Algérie  
🛣️ 45 000 km · Essence

🔗 Voir sur AutoIntel : https://autointel.dz/annonces/123

Alerte : BMW Série 3 < 25k€
```

**WhatsApp :**
```
🚗 *Bonne affaire détectée !*

🔥 15% sous le marché
*BMW Série 3 2019*
💰 22 000 € · 45 000 km
📍 Alger, Algérie · Essence

Voir : https://autointel.dz/annonces/123
(Alerte : BMW Série 3 < 25k€)
```

### 🛠️ Administration

#### Endpoints API disponibles
- `GET /api/notifications/canaux/` - Lister les canaux
- `POST /api/notifications/canaux/` - Ajouter un canal  
- `POST /api/notifications/canaux/{id}/verifier/` - Vérifier un canal
- `PATCH /api/notifications/canaux/{id}/activer/` - Activer/désactiver
- `DELETE /api/notifications/canaux/{id}/supprimer/` - Supprimer un canal
- `GET /api/notifications/status/` - Statut des services
- `GET /api/notifications/historique/` - Historique des envois

#### Tasks Celery
- `alertes.check_alertes` - Vérification automatique toutes les 6h
- `alertes.nettoyer_anciens_resultats` - Nettoyage résultats > 30 jours
- `notifications.nettoyer_historique` - Nettoyage historique > 90 jours

### 🚨 Dépannage

#### Telegram ne fonctionne pas
- Vérifiez `TELEGRAM_BOT_TOKEN` dans `.env`
- Utilisez le guide pour créer le bot correctement
- Testez avec `/start` au bot

#### WhatsApp ne fonctionne pas  
- Vérifiez les clés Twilio dans `.env`
- Assurez-vous que le numéro est au format international (`+213...`)
- Le compte Twilio doit être activé pour WhatsApp

#### Notifications non reçues
- Vérifiez que les canaux sont bien **vérifiés** et **actifs**
- Les alertes doivent être **actives** dans AutoIntel
- Vérifiez les logs Django pour les erreurs

### 📊 Monitoring

#### Dans l'admin Django
- **Canaux de notification** : Gestion complète
- **Historique des notifications** : Suivi des envois
- **Statistiques** : Taux de réussite, erreurs fréquentes

#### Logs utiles
```bash
# Logs des notifications
grep "Notification" django.log

# Logs Telegram spécifiques  
grep "Telegram" django.log

# Logs WhatsApp spécifiques
grep "WhatsApp" django.log
```

---

**Le module Alertes V2 est prêt !** 🎉

Les utilisateurs peuvent maintenant recevoir leurs alertes AutoIntel instantanément sur Telegram et WhatsApp, en plus des emails traditionnels.

**Prochain module V3 : Rapports PDF payants**
