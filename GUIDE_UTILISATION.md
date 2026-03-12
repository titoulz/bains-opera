# Guide d'utilisation - Système de Réservation
## Les Bains de l'Opéra

## 🚀 Démarrage rapide

### Méthode 1 : Script automatique (recommandé)
```bash
./start.sh
```

### Méthode 2 : Démarrage manuel

1. **Installer les dépendances**
```bash
pip3 install -r requirements.txt
```

2. **Initialiser la base de données** (première fois seulement)
```bash
python3 database.py
```

3. **Démarrer le serveur Flask (API)** dans un terminal
```bash
python3 app.py
```

4. **Démarrer le serveur web** dans un autre terminal
```bash
python3 -m http.server 8000
```

## 📱 Accès aux interfaces

- **Site web** : http://localhost:8000
- **Page de réservation** : http://localhost:8000/reservation.html
- **Interface admin** : http://localhost:8000/admin.html
- **API** : http://localhost:5000/api

## 💻 Fonctionnalités

### Pour les clients (reservation.html)

1. **Choisir une formule** parmi 4 catégories :
   - Nos Escales (MALTE, CRÈTE, RHODES, etc.)
   - Escales avec SPA (OMAN, EGÉE, BALÉARES, etc.)
   - Hammam seul
   - Massages (15min, 30min, 45min, 60min)

2. **Remplir le formulaire** :
   - Nom, prénom
   - Email, téléphone
   - Date et heure souhaitée
   - Nombre de personnes
   - Message optionnel

3. **Validation automatique** :
   - Vérification des jours fermés (Dimanche-Mardi)
   - Vérification des champs obligatoires

### Pour l'administrateur (admin.html)

1. **Tableau de bord** avec statistiques :
   - Total des réservations
   - En attente
   - Confirmées
   - Réservations du jour

2. **Liste des réservations** avec :
   - Toutes les informations client
   - Statut de chaque réservation
   - Actions disponibles

3. **Filtres disponibles** :
   - Par statut (En attente / Confirmée / Annulée)
   - Par date
   - Par formule

4. **Actions** :
   - Confirmer une réservation
   - Annuler une réservation
   - Actualiser la liste

## 🗄️ Base de données

Le fichier `reservations.db` contient :
- **reservations** : Toutes les réservations clients
- **formules** : Catalogue des 19 formules disponibles
- **creneaux** : Horaires d'ouverture

## 📊 Formules disponibles

### Nos Escales (6 formules)
- MALTE : 35€ (90min)
- CRÈTE : 45€ (105min)
- RHODES : 60€ (120min)
- SICILE : 50€ (105min)
- CHYPRE : 80€ (135min)
- CORSE : 75€ (120min)

### Escales avec SPA (6 formules)
- OMAN : 60€ (105min)
- EGÉE : 70€ (120min)
- BALÉARES : 85€ (150min)
- SUÉDOISE : 80€ (120min)
- JAVA : 90€ (135min)
- BALTIQUE : 135€ (210min)

### Hammam
- Accès hammam : 25€ (60min)

### Massages (6 formules)
- 15min : 25€
- 30min : 45€
- 45min : 65€
- 60min : 85€
- Suédois 30min : 55€
- Suédois 60min : 95€

## ⏰ Horaires

- **Mercredi** : 11h - 21h
- **Jeudi** : 11h - 19h
- **Vendredi** : 11h - 22h
- **Samedi** : 11h - 19h
- **Fermé** : Dimanche, Lundi, Mardi

## 🔧 Maintenance

### Sauvegarder la base de données
```bash
cp reservations.db reservations_backup_$(date +%Y%m%d).db
```

### Réinitialiser la base de données
```bash
rm reservations.db
python3 database.py
```

### Voir les logs Flask
```bash
# Si lancé en arrière-plan, les logs sont dans le terminal
```

## 🔒 Sécurité

**IMPORTANT pour la production** :
- Ajouter une authentification pour l'interface admin
- Utiliser HTTPS
- Configurer les emails de confirmation
- Utiliser une base de données plus robuste (PostgreSQL)
- Ajouter des validations côté serveur
- Limiter les requêtes API (rate limiting)

## 📝 Notes

- Le système fonctionne en local actuellement
- Pas d'envoi d'email automatique (à implémenter)
- Pas d'authentification admin (à sécuriser)
- SQLite est suffisant pour un usage local/démonstration
