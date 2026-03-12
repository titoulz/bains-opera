# Système de Réservation - Les Bains de l'Opéra

## Installation

### 1. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### 2. Initialiser la base de données

```bash
python database.py
```

Cette commande va créer la base de données SQLite `reservations.db` avec toutes les tables et les formules pré-configurées.

## Démarrage

### 1. Démarrer le serveur Flask (API Backend)

```bash
python app.py
```

Le serveur API sera accessible sur `http://localhost:5000`

### 2. Démarrer le serveur web (Frontend)

Dans un autre terminal :

```bash
python3 -m http.server 8000
```

Le site sera accessible sur `http://localhost:8000`

## Utilisation

### Page de réservation

Accédez à `http://localhost:8000/reservation.html` pour faire une réservation.

Fonctionnalités :
- Sélection de formule par catégorie (Escales, Escales avec SPA, Hammam, Massages)
- Formulaire de réservation avec validation
- Vérification des jours fermés (Dimanche, Lundi, Mardi)
- Confirmation par email (à configurer)

### Interface d'administration

Accédez à `http://localhost:8000/admin.html` pour gérer les réservations.

Fonctionnalités :
- Vue d'ensemble avec statistiques
- Liste de toutes les réservations
- Filtres par statut, date et formule
- Actions : Confirmer ou Annuler une réservation
- Actualisation en temps réel

## Structure de la base de données

### Table `reservations`
- id : Identifiant unique
- nom, prenom : Nom du client
- email, telephone : Contact
- formule : Nom de la formule réservée
- date_reservation : Date souhaitée
- heure_reservation : Heure souhaitée
- nombre_personnes : Nombre de personnes
- message : Message optionnel
- statut : en_attente | confirmee | annulee
- date_creation : Date de création de la réservation

### Table `formules`
- id : Identifiant unique
- nom : Nom de la formule
- type : escale | escale_spa | hammam | massage
- description : Description
- prix : Prix en euros
- duree : Durée en minutes

### Table `creneaux`
- id : Identifiant unique
- jour_semaine : Jour de la semaine
- heure_debut : Heure d'ouverture
- heure_fin : Heure de fermeture
- actif : Créneau actif ou non

## API Endpoints

### GET /api/formules
Récupère toutes les formules disponibles.
Query params : `type` (optionnel) - Filtrer par type de formule

### POST /api/reservations
Crée une nouvelle réservation.
Body : JSON avec les informations de réservation

### GET /api/reservations
Récupère toutes les réservations.

### PUT /api/reservations/:id/status
Met à jour le statut d'une réservation.
Body : `{ "statut": "confirmee" | "annulee" }`

## Horaires d'ouverture

- Mercredi : 11h - 21h
- Jeudi : 11h - 19h
- Vendredi : 11h - 22h
- Samedi : 11h - 19h
- Fermé : Dimanche, Lundi, Mardi

## Notes

- Le système utilise SQLite pour la simplicité. Pour une production, il est recommandé d'utiliser PostgreSQL ou MySQL.
- L'authentification pour l'interface admin n'est pas implémentée. À ajouter en production.
- Les emails de confirmation ne sont pas configurés. À implémenter selon les besoins.
