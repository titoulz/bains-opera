#!/usr/bin/env python3
"""Script de test pour l'envoi d'email"""

from dotenv import load_dotenv
load_dotenv()

import email_service
import database

# Récupérer une réservation de test
reservations = database.get_all_reservations()

if len(reservations) == 0:
    print("❌ Aucune réservation trouvée dans la base de données")
    print("   Créez d'abord une réservation depuis http://localhost:8000/reservation.html")
    exit(1)

# Prendre la dernière réservation
reservation = dict(reservations[0])

print("=" * 60)
print("Test d'envoi d'email")
print("=" * 60)
print(f"\nRéservation test :")
print(f"  - ID: {reservation['id']}")
print(f"  - Client: {reservation['prenom']} {reservation['nom']}")
print(f"  - Email: {reservation['email']}")
print(f"  - Formule: {reservation['formule']}")
print(f"  - Date: {reservation['date_reservation']} à {reservation['heure_reservation']}")
print(f"  - Statut: {reservation['statut']}")
print("\n" + "=" * 60)
print("Envoi de l'email de confirmation...")
print("=" * 60 + "\n")

# Tenter d'envoyer l'email
success = email_service.send_confirmation_email(reservation)

print("\n" + "=" * 60)
if success:
    print("✅ Email envoyé avec succès !")
    print(f"   Vérifiez la boîte de réception de : {reservation['email']}")
    print("   (Pensez à vérifier les spams)")
else:
    print("❌ Échec de l'envoi de l'email")
    print("   Vérifiez les logs ci-dessus pour plus de détails")
print("=" * 60)
