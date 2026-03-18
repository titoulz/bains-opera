#!/usr/bin/env python3
"""
Script d'initialisation du CMS
Ce script initialise la base de données avec le contenu par défaut
"""

import database

def init_cms():
    """Initialise le CMS avec le contenu par défaut"""
    print("Initialisation du CMS...")

    # Initialiser la base de données (crée les tables et insère les données par défaut)
    database.init_db()

    print("\n✓ Base de données initialisée avec succès!")
    print("\nLe système CMS est maintenant prêt à être utilisé.")
    print("\nPour accéder à l'interface d'administration:")
    print("1. Démarrez le serveur avec: python app.py")
    print("2. Ouvrez votre navigateur à: http://localhost:5000/login.html")
    print("3. Connectez-vous avec vos identifiants admin")
    print("4. Cliquez sur 'Gérer le contenu du site'")
    print("\nVous pourrez alors modifier:")
    print("- Les paramètres du site (horaires, contact, etc.)")
    print("- Les images du carousel de la page d'accueil")
    print("- Les formules et leurs tarifs")
    print("- Les offres spéciales du mois")

if __name__ == '__main__':
    init_cms()
