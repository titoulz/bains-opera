# Configuration de l'envoi d'emails

## Fonctionnalité

Le système envoie automatiquement un email au client lorsque l'administrateur accepte ou refuse une réservation depuis la page admin.

## Configuration

### 1. Créer le fichier de configuration

Copiez le fichier `.env.example` vers `.env` :

```bash
cp .env.example .env
```

### 2. Configurer avec Gmail

Si vous utilisez Gmail :

1. **Activer la validation en 2 étapes** sur votre compte Google
2. **Créer un mot de passe d'application** :
   - Allez sur https://myaccount.google.com/security
   - Cliquez sur "Validation en 2 étapes"
   - En bas, cliquez sur "Mots de passe d'application"
   - Sélectionnez "Application" → "Autre" → "Les Bains de l'Opéra"
   - Copiez le mot de passe généré (16 caractères)

3. **Modifier le fichier .env** :
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=votre-email@gmail.com
SMTP_PASSWORD=le-mot-de-passe-application-genere
FROM_EMAIL=votre-email@gmail.com
```

### 3. Configurer avec un autre fournisseur

#### OVH
```
SMTP_SERVER=ssl0.ovh.net
SMTP_PORT=587
SMTP_USERNAME=contact@bainsopera.com
SMTP_PASSWORD=votre-mot-de-passe
FROM_EMAIL=contact@bainsopera.com
```

#### Outlook/Hotmail
```
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=votre-email@outlook.com
SMTP_PASSWORD=votre-mot-de-passe
FROM_EMAIL=votre-email@outlook.com
```

### 4. Charger les variables d'environnement

Pour que les variables d'environnement soient chargées, modifiez le fichier `app.py` pour inclure :

```python
from dotenv import load_dotenv
load_dotenv()  # Ajouter au début du fichier
```

Installez python-dotenv :
```bash
pip3 install python-dotenv
```

## Test

Pour tester l'envoi d'emails :

1. Démarrez le serveur : `./start.sh`
2. Allez sur la page admin : http://localhost:8000/admin.html
3. Acceptez une réservation de test
4. Vérifiez que l'email a été envoyé

## Emails envoyés

### Email de confirmation (réservation acceptée)
- **Sujet** : ✓ Réservation confirmée - Les Bains de l'Opéra
- **Contenu** : Détails de la réservation, adresse, recommandations
- **Design** : Email HTML avec mise en forme professionnelle

### Email de refus (réservation refusée)
- **Sujet** : Réservation - Les Bains de l'Opéra
- **Contenu** : Message poli invitant à recontacter l'établissement

## Dépannage

### Erreur "Authentication failed"
- Vérifiez que le mot de passe d'application est correct
- Pour Gmail, assurez-vous que la validation en 2 étapes est activée

### Erreur "SMTP server not configured"
- Vérifiez que le fichier `.env` existe
- Vérifiez que les variables `SMTP_USERNAME` et `SMTP_PASSWORD` sont définies

### Email non reçu
- Vérifiez le dossier spam
- Vérifiez les logs du serveur Flask
- Testez avec une autre adresse email

## Sécurité

⚠️ **Important** :
- Ne JAMAIS committer le fichier `.env` dans Git
- Le fichier `.gitignore` contient déjà `.env` pour éviter cela
- Gardez vos identifiants SMTP confidentiels
