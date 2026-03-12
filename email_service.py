import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# Configuration SMTP (à personnaliser)
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')  # Email de l'établissement
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')  # Mot de passe d'application
FROM_EMAIL = os.getenv('FROM_EMAIL', 'contact@bainsopera.com')
FROM_NAME = "Les Bains de l'Opéra"

def format_date_fr(date_str):
    """Formate une date en français"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
        mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin',
                'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

        jour_semaine = jours[date_obj.weekday()]
        jour = date_obj.day
        mois_nom = mois[date_obj.month - 1]
        annee = date_obj.year

        return f"{jour_semaine} {jour} {mois_nom} {annee}"
    except:
        return date_str

def send_confirmation_email(reservation):
    """
    Envoie un email de confirmation au client lorsque sa réservation est acceptée

    Args:
        reservation: dict contenant les informations de la réservation
    """

    # Vérifier que les paramètres SMTP sont configurés
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print("⚠️  Configuration SMTP manquante. Email non envoyé.")
        print("   Configurez les variables d'environnement SMTP_USERNAME et SMTP_PASSWORD")
        return False

    try:
        # Créer le message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"✓ Réservation confirmée - Les Bains de l'Opéra"
        msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg['To'] = reservation['email']

        # Formater la date
        date_formatee = format_date_fr(reservation['date_reservation'])

        # Corps de l'email en HTML
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .header {{
                    background: linear-gradient(135deg, #D4915E 0%, #8B8B5E 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .info-box {{
                    background: white;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 8px;
                    border-left: 4px solid #D4915E;
                }}
                .info-row {{
                    display: flex;
                    padding: 10px 0;
                    border-bottom: 1px solid #eee;
                }}
                .info-label {{
                    font-weight: bold;
                    color: #D4915E;
                    min-width: 150px;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    color: #666;
                    font-size: 12px;
                }}
                .cta-button {{
                    display: inline-block;
                    background: #D4915E;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 25px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>✓ Réservation Confirmée</h1>
                <p>Les Bains de l'Opéra</p>
            </div>

            <div class="content">
                <p>Bonjour {reservation['prenom']} {reservation['nom']},</p>

                <p>Nous avons le plaisir de vous confirmer votre réservation aux Bains de l'Opéra.</p>

                <div class="info-box">
                    <h3 style="margin-top: 0; color: #D4915E;">Détails de votre réservation</h3>

                    <div class="info-row">
                        <span class="info-label">Formule :</span>
                        <span>{reservation['formule']}</span>
                    </div>

                    <div class="info-row">
                        <span class="info-label">Date :</span>
                        <span>{date_formatee}</span>
                    </div>

                    <div class="info-row">
                        <span class="info-label">Heure :</span>
                        <span>{reservation['heure_reservation']}</span>
                    </div>

                    <div class="info-row" style="border-bottom: none;">
                        <span class="info-label">Nombre de personnes :</span>
                        <span>{reservation['nombre_personnes']}</span>
                    </div>
                </div>

                <h3 style="color: #D4915E;">Informations pratiques</h3>
                <p><strong>Adresse :</strong><br>
                Les Bains de l'Opéra<br>
                20 Rue Joseph Serlin<br>
                69001 Lyon</p>

                <p><strong>Recommandations :</strong></p>
                <ul>
                    <li>Merci d'arriver 10 minutes avant l'heure de votre rendez-vous</li>
                    <li>Pensez à apporter votre maillot de bain et une serviette</li>
                    <li>Pour toute modification ou annulation, contactez-nous au moins 24h à l'avance</li>
                </ul>

                <p style="margin-top: 30px;">Nous vous attendons avec plaisir pour ce moment de détente et de bien-être.</p>

                <p style="margin-top: 20px;">
                    <strong>Besoin de nous contacter ?</strong><br>
                    Téléphone : 04 XX XX XX XX<br>
                    Email : contact@bainsopera.com
                </p>
            </div>

            <div class="footer">
                <p>&copy; 2026 Les Bains de l'Opéra - Tous droits réservés</p>
                <p>HAMMAM RÉSERVÉ AUX FEMMES</p>
            </div>
        </body>
        </html>
        """

        # Version texte simple (fallback)
        text_body = f"""
Réservation Confirmée - Les Bains de l'Opéra

Bonjour {reservation['prenom']} {reservation['nom']},

Nous avons le plaisir de vous confirmer votre réservation aux Bains de l'Opéra.

Détails de votre réservation :
- Formule : {reservation['formule']}
- Date : {date_formatee}
- Heure : {reservation['heure_reservation']}
- Nombre de personnes : {reservation['nombre_personnes']}

Adresse :
Les Bains de l'Opéra
20 Rue Joseph Serlin
69001 Lyon

Recommandations :
- Merci d'arriver 10 minutes avant l'heure de votre rendez-vous
- Pensez à apporter votre maillot de bain et une serviette
- Pour toute modification ou annulation, contactez-nous au moins 24h à l'avance

Nous vous attendons avec plaisir pour ce moment de détente et de bien-être.

Contact :
Téléphone : 04 XX XX XX XX
Email : contact@bainsopera.com

---
Les Bains de l'Opéra
HAMMAM RÉSERVÉ AUX FEMMES
        """

        # Attacher les deux versions
        part1 = MIMEText(text_body, 'plain', 'utf-8')
        part2 = MIMEText(html_body, 'html', 'utf-8')
        msg.attach(part1)
        msg.attach(part2)

        # Envoyer l'email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.set_debuglevel(0)
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"✓ Email de confirmation envoyé à {reservation['email']}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"✗ Erreur d'authentification SMTP : {str(e)}")
        print("   Vérifiez SMTP_USERNAME et SMTP_PASSWORD")
        return False
    except smtplib.SMTPException as e:
        print(f"✗ Erreur SMTP : {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Erreur lors de l'envoi de l'email : {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def send_rejection_email(reservation):
    """
    Envoie un email au client lorsque sa réservation est refusée

    Args:
        reservation: dict contenant les informations de la réservation
    """

    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print("⚠️  Configuration SMTP manquante. Email non envoyé.")
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Réservation - Les Bains de l'Opéra"
        msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg['To'] = reservation['email']

        date_formatee = format_date_fr(reservation['date_reservation'])

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .header {{
                    background: linear-gradient(135deg, #8B8B5E 0%, #666 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Réservation - Les Bains de l'Opéra</h1>
            </div>

            <div class="content">
                <p>Bonjour {reservation['prenom']} {reservation['nom']},</p>

                <p>Nous vous remercions pour votre demande de réservation pour le {date_formatee} à {reservation['heure_reservation']}.</p>

                <p>Malheureusement, nous ne pouvons pas donner suite à votre demande pour ce créneau. Nous vous invitons à nous contacter directement pour trouver une alternative qui vous conviendrait.</p>

                <p><strong>Contact :</strong><br>
                Téléphone : 04 XX XX XX XX<br>
                Email : contact@bainsopera.com</p>

                <p>Nous restons à votre disposition et espérons vous accueillir prochainement.</p>

                <p>Cordialement,<br>
                L'équipe des Bains de l'Opéra</p>
            </div>
        </body>
        </html>
        """

        text_body = f"""
Bonjour {reservation['prenom']} {reservation['nom']},

Nous vous remercions pour votre demande de réservation pour le {date_formatee} à {reservation['heure_reservation']}.

Malheureusement, nous ne pouvons pas donner suite à votre demande pour ce créneau. Nous vous invitons à nous contacter directement pour trouver une alternative qui vous conviendrait.

Contact :
Téléphone : 04 XX XX XX XX
Email : contact@bainsopera.com

Nous restons à votre disposition et espérons vous accueillir prochainement.

Cordialement,
L'équipe des Bains de l'Opéra
        """

        part1 = MIMEText(text_body, 'plain', 'utf-8')
        part2 = MIMEText(html_body, 'html', 'utf-8')
        msg.attach(part1)
        msg.attach(part2)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.set_debuglevel(0)
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"✓ Email de refus envoyé à {reservation['email']}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"✗ Erreur d'authentification SMTP : {str(e)}")
        print("   Vérifiez SMTP_USERNAME et SMTP_PASSWORD")
        return False
    except smtplib.SMTPException as e:
        print(f"✗ Erreur SMTP : {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Erreur lors de l'envoi de l'email : {str(e)}")
        import traceback
        traceback.print_exc()
        return False
