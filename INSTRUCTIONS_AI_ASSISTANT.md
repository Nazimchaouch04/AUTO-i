# AUTOINTEL AI ASSISTANT - GUIDE D'INSTALLATION

## ✅ Module V1 Terminé

Le module AI Assistant est maintenant entièrement intégré à AutoIntel !

### 🚀 Fonctionnalités implémentées

#### Backend
- ✅ **App Django** `apps/ai_assistant/` avec modèles Conversation, Message, UsageIA
- ✅ **Service Claude API** avec contexte marché en temps réel
- ✅ **Endpoints REST** pour conversations, messages, stats
- ✅ **Limites d'utilisation** (5 messages/jour gratuits, illimité Pro)
- ✅ **Système de prompts** intelligent basé sur les données du marché

#### Frontend
- ✅ **Page Assistant** complète (`/assistant`) avec chat 2 colonnes
- ✅ **Bouton flottant AI** sur toutes les pages
- ✅ **Messages suggérés** contextuels selon la page
- ✅ **Rendu Markdown** pour les réponses de l'assistant
- ✅ **Intégration navigation** (header + menu mobile)

### 🔧 Configuration requise

1. **Variables d'environnement** (créer `.env` dans `backend/`) :
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
```

2. **Dépendances installées** :
```bash
# Backend
pip install anthropic

# Frontend  
npm install react-markdown
```

3. **Base de données** :
```bash
python manage.py migrate
```

### 🎯 Utilisation

#### Accès à l'assistant
- **Page complète** : `/assistant` (réservé aux utilisateurs connectés)
- **Bouton flottant** : Disponible sur toutes les pages
- **Navigation** : Lien "AI Assistant" dans le header

#### Fonctionnalités
- **Questions automobiles** : Prix, tendances, conseils d'achat
- **Contexte marché** : Basé sur les vraies données d'AutoIntel
- **Limites gratuites** : 5 messages/jour, puis upgrade Pro
- **Historique** : Conversations sauvegardées

#### Messages suggérés
- Sur page annonces : "Analyse cette annonce pour moi"
- Sur page estimation : "Explique ce résultat"  
- Sur dashboard : "Résume le marché du moment"

### 🔄 Prochaines étapes (V2-V5)

Le module V1 est fonctionnel. Pour continuer :

1. **V2** : Alertes WhatsApp & Telegram
2. **V3** : Rapports PDF payants  
3. **V4** : Dashboard concessionnaires B2B
4. **V5** : Analytics avancés + B2B

### 🐛 Dépannage

#### Claude API ne fonctionne pas
- Vérifiez `ANTHROPIC_API_KEY` dans `.env`
- Assurez-vous que la clé API est valide et active

#### Frontend ne se charge pas
- Vérifiez que `react-markdown` est installé
- Redémarrez le serveur de développement

#### Erreur de migration
- Supprimez `db.sqlite3` et relancez `python manage.py migrate`

---

**Le module AI Assistant V1 est prêt ! 🎉**
