# 🔐 **Identifiants Admin AutoIntel**

## **📧 Email et Mot de Passe Admin:**

### **Super-utilisateur par défaut:**
- **Email:** `admin@autointel.com`
- **Mot de passe:** `AutoIntel2024!`
- **Nom d'utilisateur:** `admin`

## **🚀 Commande pour créer le super-utilisateur:**

```bash
cd backend
python manage.py createsuperuser
```

**Répondez avec:**
- Username: `admin`
- Email address: `admin@autointel.com`
- Password: `AutoIntel2024!`
- Password (again): `AutoIntel2024!`

## **🌐 Accès Administration:**

### **URL Admin Django:**
```
http://localhost:8000/admin/
```

### **Accès rapide:**
1. Lancez le serveur: `python manage.py runserver`
2. Ouvrez: `http://localhost:8000/admin/`
3. Connectez-vous avec les identifiants ci-dessus

## **📋 Fonctionnalités Admin:**

### **Gestion des modèles:**
- ✅ **Marques** - Ajouter/modifier les constructeurs
- ✅ **Modèles** - Gérer les modèles de véhicules  
- ✅ **Annonces** - Voir/gérer toutes les annonces
- ✅ **Images** - Gérer les photos des véhicules
- ✅ **Estimations** - Voir les estimations ML
- ✅ **Alertes** - Gérer les alertes utilisateurs

### **Actions disponibles:**
- Créer/éditer/supprimer des marques
- Importer des données en masse
- Voir les statistiques
- Gérer les utilisateurs Django

## **🔒 Sécurité:**

**Pour la production:**
- Changez le mot de passe par défaut
- Utilisez un email réel
- Activez HTTPS

## **🎯 Étapes suivantes:**

1. **Créer le super-utilisateur** avec les identifiants ci-dessus
2. **Démarrer le serveur** Django
3. **Se connecter** à l'interface admin
4. **Commencer à gérer** les données AutoIntel

**L'interface admin Django vous donnera un contrôle total sur toutes les données de la plateforme!** 🎉
