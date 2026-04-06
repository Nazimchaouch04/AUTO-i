# 🤖 Guide Création Bot Telegram AutoIntel

## Étape 1 : Créer le Bot sur Telegram

1. **Ouvrez Telegram** et cherchez **@BotFather**
2. **Envoyez `/newbot`** pour créer un nouveau bot
3. **Donnez un nom** : `AutoIntel Bot` (ou votre préférence)
4. **Donnez un username** : `AutoIntelBot` (doit finir par "Bot")
5. **Copiez le token** qui vous sera fourni (format : `1234567890:ABCDEF...`)

## Étape 2 : Configurer le Bot

1. **Ajoutez le token** dans votre `.env` :
   ```bash
   TELEGRAM_BOT_TOKEN=1234567890:ABCDEF...
   ```

2. **Redémarrez le serveur Django** pour appliquer la configuration

## Étape 3 : Obtenir votre Chat ID

1. **Cherchez votre bot** sur Telegram (ex: `@AutoIntelBot`)
2. **Envoyez `/start`** pour démarrer la conversation
3. **Envoyez n'importe quel message** pour activer le chat
4. **Pour obtenir votre Chat ID** :
   - Option A : Envoyez `/start` à **@userinfobot**
   - Option B : Envoyez un message à **@RawDataBot**
   - Option C : Utilisez **@get_id_bot**

5. **Notez votre Chat ID** (format : `123456789`)

## Étape 4 : Connecter le Bot à AutoIntel

1. **Connectez-vous** à votre application AutoIntel
2. **Allez dans "Alertes"** → "Notifications"**
3. **Dans la section Telegram** :
   - Entrez votre Chat ID (ex: `123456789`)
   - Cliquez sur "Connecter Telegram"
4. **Cliquez sur "Vérifier"** pour tester la connexion

## Étape 5 : Vérifier le Fonctionnement

1. **Le bot devrait vous envoyer** un message de test
2. **Créez une alerte** dans AutoIntel
3. **Attendez** qu'une nouvelle annonce corresponde à vos critères
4. **Vous devriez recevoir** une notification sur Telegram

## 🔧 Commandes du Bot (Optionnel)

Vous pouvez ajouter des commandes personnalisées dans `apps/notifications/telegram_service.py` :

```python
# Commandes disponibles
/start - Message de bienvenue
/help - Aide et instructions
/status - Vérifier le statut du bot
/alertes - Lister les alertes actives
```

## 🛠️ Configuration Avancée

### Webhook (Production)
Pour la production, configurez un webhook :

```python
# Dans telegram_service.py
WEBHOOK_URL = "https://votre-domaine.com/api/telegram/webhook/"

# Configuration du webhook
url = f'{TELEGRAM_API}/setWebhook'
payload = {
    'url': WEBHOOK_URL,
    'allowed_updates': ['message', 'callback_query']
}
```

### Personnalisation des Messages

Modifiez les templates dans `formater_alerte_telegram()` :

```python
# Personnalisez le format des messages
message = f"""🚗 <b>Votre titre personnalisé</b>

{votre_contenu_personnalisé}

🔗 Lien : {annonce_url}"""
```

## 🚨 Dépannage

### Problèmes Communs

**Bot ne répond pas :**
- Vérifiez que le token est correct
- Redémarrez le serveur Django
- Vérifiez les logs Django

**Chat ID invalide :**
- Utilisez @RawDataBot pour vérifier votre ID
- Assurez-vous d'utiliser des chiffres uniquement

**Messages non reçus :**
- Vérifiez que le bot n'est pas bloqué par Telegram
- Testez avec `/start` au bot

### Logs Utiles

```bash
# Logs Django pour voir les erreurs
python manage.py runserver --verbosity=2

# Logs spécifiques Telegram
grep "Telegram" django.log
```

## 📱 Exemples de Messages

**Message de bienvenue :**
```
🎉 Bienvenue sur AutoIntel Bot !

Je suis votre assistant personnel pour chasser les meilleures affaires automobiles.

Configurez vos alertes sur AutoIntel et je vous préviendrai instantanément dès qu'une pépite apparaît.

/start pour commencer
/help pour l'aide
```

**Message d'alerte :**
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

---

**Votre bot Telegram est maintenant prêt !** 🚀

Pour toute question : consultez la documentation technique ou contactez le support.
