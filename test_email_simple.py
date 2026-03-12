import os
from dotenv import load_dotenv

load_dotenv()

print("=== Configuration SMTP ===")
print(f"SMTP_SERVER: {os.getenv('SMTP_SERVER', 'NOT SET')}")
print(f"SMTP_PORT: {os.getenv('SMTP_PORT', 'NOT SET')}")
print(f"SMTP_USERNAME: {os.getenv('SMTP_USERNAME', 'NOT SET')}")
print(f"SMTP_PASSWORD: {'***' if os.getenv('SMTP_PASSWORD') else 'NOT SET'}")
print(f"FROM_EMAIL: {os.getenv('FROM_EMAIL', 'NOT SET')}")
print(f"EMAIL_TO: {os.getenv('EMAIL_TO', 'NOT SET')}")

# Test d'envoi
if os.getenv('SMTP_USERNAME') and os.getenv('SMTP_PASSWORD'):
    print("\n=== Test d'envoi ===")
    reservation_test = {
        'prenom': 'Test',
        'nom': 'User',
        'email': os.getenv('EMAIL_TO', 'test@example.com'),
        'formule': 'HAMMAM',
        'date_reservation': '2026-03-15',
        'heure_reservation': '14:00',
        'nombre_personnes': 1
    }

    import email_service
    result = email_service.send_confirmation_email(reservation_test)
    print(f"Résultat: {'✓ SUCCESS' if result else '✗ FAILED'}")
else:
    print("\n⚠️  Variables SMTP manquantes, impossible de tester l'envoi")
