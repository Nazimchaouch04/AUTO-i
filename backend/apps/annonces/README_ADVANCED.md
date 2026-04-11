# Backend Avancé - AutoIntel Annonces

## 🚀 Nouvelles Fonctionnalités Implémentées

### 1. Système de Recherche Avancée
- **Recherche intelligente** avec suggestions automatiques
- **Filtres multiples** : prix, kilométrage, année, marque, modèle, carburant, etc.
- **Historique des recherches** sauvegardé
- **Recherche sauvegardable** avec nom personnalisé

### 2. Système de Recommandations IA
- **Moteur de recommandations** basé sur le comportement utilisateur
- **5 types de recommandations** :
  - Basées sur l'historique de navigation
  - Basées sur les favoris
  - Basées sur les recherches
  - Basées sur les contacts
  - Annonces populaires (fallback)
- **Personnalisation** selon les préférences

### 3. Gestion Avancée des Favoris
- **Ajout/Retrait** des favoris en un clic
- **Statistiques** sur les favoris
- **Comparaison** des favoris
- **Export** des favoris en CSV

### 4. Système de Notifications Intelligent
- **Notifications personnalisées** selon l'activité
- **Types de notifications** :
  - Nouvelles annonces correspondantes
  - Baisse de prix
  - Bonnes affaires détectées
  - Nouveaux contacts
- **Gestion** des notifications lues/non lues

### 5. Alertes de Recherche Automatisées
- **Création d'alertes** avec filtres personnalisés
- **Fréquences** : immédiat, quotidien, hebdomadaire
- **Notifications automatiques** lors de nouvelles annonces
- **Historique** des alertes

### 6. Analytics et Statistiques Avancées
- **Tableau de bord utilisateur** avec statistiques personnelles
- **Insights du marché** en temps réel
- **Tendances** des prix et popularité
- **Export** des statistiques personnelles

### 7. Système d'Évaluation des Vendeurs
- **Évaluation** après contact (note 1-5 étoiles)
- **Commentaires** et aspects détaillés
- **Statistiques** des vendeurs
- **Fiabilité** et confiance

### 8. Signalement d'Annonces
- **Signalement** pour annonces abusives
- **Motifs** prédéfinis
- **Suivi** des signalements
- **Modération** intégrée

### 9. Optimisation des Performances
- **Système de cache** intelligent
- **Préchauffage** du cache
- **Invalidation** automatique
- **Middleware** de gestion du cache

### 10. Tâches Automatisées
- **Mise à jour** des recommandations périodique
- **Traitement** des alertes automatique
- **Nettoyage** des anciennes données
- **Notifications** des bonnes affaires

---

## 📁 Structure des Fichiers

```
apps/annonces/
├── models.py                 # Modèles de base
├── models_advanced.py         # Modèles avancés
├── views.py                 # Vues de base
├── views_advanced.py         # Vues avancées
├── views_recommandations.py  # Vues de recommandations
├── serializers.py           # Sérialiseurs de base
├── serializers_advanced.py   # Sérialiseurs avancés
├── services.py             # Services métier
├── cache_manager.py        # Gestion du cache
├── tasks.py               # Tâches Celery
├── urls.py               # URLs de base
├── urls_advanced.py       # URLs avancées
└── README_ADVANCED.md     # Cette documentation
```

---

## 🔌 Nouveaux Endpoints API

### Recherche et Filtres
- `GET /api/annonces/search/advanced/` - Recherche avancée
- `GET /api/annonces/search/suggestions/` - Suggestions de recherche
- `POST /api/annonces/recherche/sauvegarder/` - Sauvegarder recherche

### Recommandations
- `GET /api/annonces/recommendations/` - Recommandations personnalisées
- `GET /api/annonces/dashboard/user/` - Dashboard utilisateur
- `GET /api/annonces/insights/market/` - Insights du marché

### Actions Utilisateur
- `POST /api/annonces/{id}/ajouter_favori/` - Ajouter aux favoris
- `DELETE /api/annonces/{id}/retirer_favori/` - Retirer des favoris
- `POST /api/annonces/{id}/contacter_vendeur/` - Contacter vendeur
- `POST /api/annonces/{id}/signaler/` - Signaler annonce
- `POST /api/annonces/{id}/evaluer_vendeur/` - Évaluer vendeur

### Export et Statistiques
- `GET /api/annonces/export/export_favoris/` - Exporter favoris CSV
- `GET /api/annonces/export/export_statistiques/` - Exporter stats JSON
- `GET /api/annonces/mes_favoris/` - Liste des favoris
- `GET /api/annonces/mes_contacts/` - Historique des contacts

### Notifications
- `GET /api/annonces/dashboard/user/` - Notifications non lues
- `GET /api/annonces/actions/quick/` - Actions rapides

---

## 🎯 Fonctionnalités Clés

### Moteur de Recommandations
Le système analyse le comportement utilisateur pour proposer des annonces pertinentes :

```python
# Exemple d'utilisation
engine = RecommendationEngine(user)
recommendations = engine.get_recommendations(limit=10)
```

### Cache Intelligent
Système de cache pour optimiser les performances :

```python
# Utilisation du cache
stats = CacheManager.get_market_stats()
popular = CacheManager.get_popular_annonces(limit=10)
```

### Tâches Automatisées
Tâches périodiques pour maintenir le système à jour :

```python
# Configuration Celery
CELERYBEAT_SCHEDULE = {
    'update-recommendations': {
        'task': 'annonces.update_recommendations',
        'schedule': crontab(minute=0, hour='*/6'),
    },
}
```

---

## 📊 Modèles de Données Avancés

### HistoriqueRecherche
- Suivi des recherches utilisateur
- Filtres sauvegardés
- Nombre de résultats

### Signalement
- Signalement d'annonces abusives
- Suivi de traitement
- Modération intégrée

### NotificationAnnonce
- Notifications personnalisées
- Types multiples
- État lu/non lu

### EvaluationVendeur
- Évaluation après contact
- Note 1-5 étoiles
- Commentaires et aspects

### VisiteAnnonce
- Suivi des visites
- Analytics détaillés
- Durée de visite

---

## 🚀 Performance et Optimisation

### Cache Stratégies
- **Market stats** : 5 minutes
- **Popular annonces** : 10 minutes
- **User recommendations** : 30 minutes
- **Search suggestions** : 15 minutes

### Indexation de Base de Données
- Index sur les champs fréquemment recherchés
- Index composites pour les requêtes complexes
- Optimisation des jointures

### Tâches Planifiées
- Mise à jour des recommandations : toutes les 6 heures
- Traitement des alertes : toutes les 2 heures
- Nettoyage des données : hebdomadaire

---

## 🔧 Configuration

### Variables d'Environnement
```bash
# Cache
CACHE_TTL=300
CACHE_BACKEND=redis

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Installation Dépendances
```bash
pip install redis celery django-redis
```

---

## 📈 Monitoring et Analytics

### Métriques Disponibles
- Taux de conversion des recommandations
- Performance du cache
- Fréquence des recherches
- Engagement utilisateur

### Tableaux de Bord
- Dashboard utilisateur personnalisé
- Analytics du marché en temps réel
- Statistiques des vendeurs

---

## 🔄 Mises à Jour Futures

1. **Machine Learning avancé** pour les recommandations
2. **API GraphQL** pour des requêtes plus efficaces
3. **WebSocket** pour les notifications en temps réel
4. **Export avancé** avec plus de formats
5. **Analytics prédictifs** pour les tendances

---

## 📝 Notes de Développement

### Bonnes Pratiques
- Utilisation du cache pour toutes les données fréquentes
- Validation des entrées utilisateur
- Gestion des erreurs robuste
- Logging complet pour le debugging

### Sécurité
- Validation des permissions
- Protection contre les abus
- Rate limiting sur les endpoints critiques
- Nettoyage automatique des données sensibles

---

## 🎉 Conclusion

Ce backend avancé offre une expérience utilisateur riche et personnalisée avec des performances optimisées. Le système de recommandations intelligent, couplé aux analytics détaillés et aux notifications automatisées, crée une plateforme moderne et engageante pour l'achat et la vente de véhicules.
