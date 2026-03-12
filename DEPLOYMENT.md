# Guide de déploiement sur Render

## Étapes de déploiement

### 1. Préparer le repo GitHub

Le repo est maintenant prêt avec tous les fichiers nécessaires :
- `render.yaml` : Configuration Render
- `Procfile` : Commande de démarrage
- `requirements.txt` : Dépendances Python
- `.gitignore` : Fichiers à ignorer

### 2. Créer le service sur Render

1. Connectez-vous à [render.com](https://render.com)
2. Cliquez sur "New +" et sélectionnez "Web Service"
3. Connectez votre repo GitHub
4. Render détectera automatiquement le fichier `render.yaml`

### 3. Configurer les variables d'environnement

Dans les paramètres de votre service Render, ajoutez ces variables :

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=votre-email@gmail.com
SMTP_PASSWORD=votre-mot-de-passe-application
EMAIL_FROM=votre-email@gmail.com
EMAIL_TO=contact@bains-opera.fr
```

**Important** : Pour Gmail, utilisez un "Mot de passe d'application" et non votre mot de passe normal.

### 4. Déployer

Render déploiera automatiquement votre application. Le processus prend environ 5 minutes.

### 5. Accéder à votre application

Une fois déployé, Render vous fournira une URL du type :
`https://bains-opera.onrender.com`

### 6. Mettre à jour les URLs dans vos fichiers HTML

Dans vos fichiers HTML (reservation.html, etc.), remplacez :
```javascript
const API_URL = 'http://localhost:5000';
```

par :
```javascript
const API_URL = 'https://votre-app.onrender.com';
```

## Base de données

La base de données SQLite (`reservations.db`) est incluse dans le repo et sera déployée avec l'application.

**Important** : Sur le plan gratuit de Render, la base de données sera réinitialisée à chaque redéploiement. Pour une solution permanente, envisagez :
- Utiliser PostgreSQL (Render propose une base gratuite)
- Passer au plan payant avec stockage persistant

## Notes importantes

- Le plan gratuit de Render met l'application en veille après 15 minutes d'inactivité
- Le premier chargement après la mise en veille peut prendre 30-60 secondes
- Pour une performance constante, envisagez le plan payant ($7/mois)

## Domaine personnalisé

Pour utiliser votre propre domaine :
1. Allez dans les paramètres de votre service Render
2. Section "Custom Domain"
3. Ajoutez votre domaine et configurez les DNS selon les instructions

## Surveillance

Render fournit :
- Logs en temps réel
- Métriques de performance
- Alertes par email en cas de problème
