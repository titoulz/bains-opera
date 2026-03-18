# CMS pour Les Bains de l'Opéra - Documentation Technique

## 🎯 Vue d'ensemble

Ce système CMS (Content Management System) permet à votre tante de gérer facilement le contenu du site sans toucher au code. Le système est intégré au site existant et utilise Flask, SQLite et Bootstrap.

## 📁 Architecture

### Fichiers ajoutés

```
├── database.py              # Fonctions CRUD pour le CMS (modifié)
├── app.py                   # Endpoints API pour le CMS (modifié)
├── admin-content.html       # Interface d'administration CMS (nouveau)
├── admin.html              # Lien vers la gestion de contenu (modifié)
├── content-loader.js        # Script de chargement dynamique (nouveau)
├── init_cms.py             # Script d'initialisation (nouveau)
├── GUIDE_CMS.md            # Guide utilisateur pour votre tante (nouveau)
└── index.html              # Utilise content-loader.js (modifié)
```

### Base de données

Nouvelles tables ajoutées à `reservations.db` :

1. **site_settings** : Paramètres généraux (horaires, contact, etc.)
2. **carousel_images** : Images du carousel de la page d'accueil
3. **content_sections** : Sections de contenu personnalisables
4. **special_offers** : Offres spéciales temporaires

## 🚀 Installation et Démarrage

### 1. Initialiser le CMS

```bash
python3 init_cms.py
```

Cette commande :
- Crée toutes les tables nécessaires
- Insère les données par défaut
- Affiche un message de confirmation

### 2. Démarrer le serveur

```bash
python3 app.py
```

Le serveur démarre sur `http://localhost:5000`

### 3. Accéder à l'interface CMS

1. Allez sur `http://localhost:5000/login.html`
2. Connectez-vous avec les identifiants admin
3. Cliquez sur "Gérer le contenu du site"

## 📡 API Endpoints

### Paramètres du site

- `GET /api/cms/settings` - Récupère tous les paramètres
- `PUT /api/cms/settings` - Met à jour les paramètres (protégé)

### Carousel

- `GET /api/cms/carousel` - Images actives du carousel
- `GET /api/cms/carousel/all` - Toutes les images (protégé)
- `POST /api/cms/carousel` - Créer une image (protégé)
- `PUT /api/cms/carousel/<id>` - Modifier une image (protégé)
- `DELETE /api/cms/carousel/<id>` - Supprimer une image (protégé)

### Sections de contenu

- `GET /api/cms/content?page=<page>` - Récupère les sections d'une page
- `GET /api/cms/content/<page>/<section_key>` - Récupère une section spécifique
- `PUT /api/cms/content` - Met à jour une section (protégé)

### Offres spéciales

- `GET /api/cms/offers` - Offres actives
- `GET /api/cms/offers/all` - Toutes les offres (protégé)
- `POST /api/cms/offers` - Créer une offre (protégé)
- `PUT /api/cms/offers/<id>` - Modifier une offre (protégé)
- `DELETE /api/cms/offers/<id>` - Supprimer une offre (protégé)

### Formules

- `GET /api/cms/formules` - Toutes les formules (protégé)
- `POST /api/cms/formules` - Créer une formule (protégé)
- `PUT /api/cms/formules/<id>` - Modifier une formule (protégé)
- `DELETE /api/cms/formules/<id>` - Supprimer une formule (protégé)

## 🔐 Sécurité

- Tous les endpoints de modification sont protégés par authentification JWT
- Le token est vérifié via le décorateur `@auth.token_required`
- Les endpoints publics (GET) ne nécessitent pas d'authentification

## 🎨 Frontend

### content-loader.js

Ce script est chargé sur toutes les pages et :
1. Charge les paramètres du site au chargement
2. Met à jour les horaires, adresse, contact
3. Sur la page d'accueil :
   - Charge le carousel dynamiquement
   - Affiche les offres spéciales actives

### admin-content.html

Interface Bootstrap 5 avec 4 onglets :
1. **Paramètres** : Formulaire pour modifier les infos du site
2. **Carousel** : Tableau avec CRUD pour les images
3. **Formules & Tarifs** : Tableau avec CRUD pour les formules
4. **Offres Spéciales** : Tableau avec CRUD pour les offres

## 📦 Déploiement

### Render.com (Production actuelle)

Le système est déjà configuré pour Render. Aucune modification n'est nécessaire dans `render.yaml`.

1. **Push du code sur Git :**
   ```bash
   git add .
   git commit -m "Add CMS system"
   git push
   ```

2. **Render redéploiera automatiquement**

3. **Initialiser le CMS en production :**
   - Connectez-vous au shell Render
   - Exécutez : `python init_cms.py`

### Variables d'environnement

Aucune nouvelle variable nécessaire. Le système utilise les mêmes que l'application existante.

## 🔧 Maintenance

### Sauvegarder la base de données

```bash
cp reservations.db reservations_backup_$(date +%Y%m%d).db
```

### Réinitialiser le CMS (⚠️ Attention : efface les modifications)

```bash
rm reservations.db
python3 init_cms.py
```

### Ajouter de nouvelles sections de contenu

1. Modifier `database.py` pour ajouter des fonctions si nécessaire
2. Créer les endpoints dans `app.py`
3. Ajouter l'interface dans `admin-content.html`
4. Mettre à jour `content-loader.js` pour charger le contenu

## 📋 Fonctionnalités futures possibles

- [ ] Upload d'images directement depuis l'interface (actuellement besoin de FTP)
- [ ] Éditeur WYSIWYG pour les descriptions (actuellement textarea simple)
- [ ] Gestion des pages complètes (hammam.html, massages.html, etc.)
- [ ] Système de templates pour les emails
- [ ] Historique des modifications
- [ ] Multi-utilisateurs avec permissions

## 🐛 Debugging

### Vérifier les tables

```bash
sqlite3 reservations.db ".schema site_settings"
```

### Voir les données

```bash
sqlite3 reservations.db "SELECT * FROM site_settings;"
sqlite3 reservations.db "SELECT * FROM carousel_images;"
```

### Logs de l'API

Les logs sont affichés dans la console où Flask est exécuté.

## 💡 Conseils pour votre tante

1. **Formation** : Montrez-lui le GUIDE_CMS.md et faites une démonstration
2. **Pratique** : Créez une offre test ensemble
3. **Sauvegardes** : Faites des sauvegardes régulières de la base
4. **Support** : Soyez disponible pour les premières utilisations

## 📞 Contact

Pour toute question technique, référez-vous à ce README ou contactez l'administrateur système.

---

**Bon courage avec le CMS !** 🚀
