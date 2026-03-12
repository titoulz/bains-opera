from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from dotenv import load_dotenv
import database
import email_service
import json
from datetime import datetime

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"], "allow_headers": ["Content-Type"]}})

# Initialiser la base de données au démarrage
database.init_db()

@app.route('/')
def index():
    return "API de réservation - Les Bains de l'Opéra"

@app.route('/api/formules', methods=['GET'])
def get_formules():
    """Récupère toutes les formules disponibles"""
    type_formule = request.args.get('type')
    formules = database.get_formules_by_type(type_formule)

    formules_list = []
    for formule in formules:
        formules_list.append({
            'id': formule[0],
            'nom': formule[1],
            'type': formule[2],
            'description': formule[3],
            'prix': formule[4],
            'duree': formule[5]
        })

    return jsonify(formules_list)

@app.route('/api/reservations', methods=['POST'])
def create_reservation():
    """Crée une nouvelle réservation"""
    data = request.get_json()

    required_fields = ['nom', 'prenom', 'email', 'telephone', 'formule', 'date_reservation', 'heure_reservation']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Le champ {field} est requis'}), 400

    try:
        reservation_id = database.create_reservation(
            nom=data['nom'],
            prenom=data['prenom'],
            email=data['email'],
            telephone=data['telephone'],
            formule=data['formule'],
            date_reservation=data['date_reservation'],
            heure_reservation=data['heure_reservation'],
            nombre_personnes=data.get('nombre_personnes', 1),
            message=data.get('message', '')
        )

        return jsonify({
            'success': True,
            'message': 'Réservation créée avec succès',
            'reservation_id': reservation_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reservations', methods=['GET'])
def get_reservations():
    """Récupère toutes les réservations"""
    reservations = database.get_all_reservations()

    reservations_list = []
    for reservation in reservations:
        reservations_list.append({
            'id': reservation['id'],
            'nom': reservation['nom'],
            'prenom': reservation['prenom'],
            'email': reservation['email'],
            'telephone': reservation['telephone'],
            'formule': reservation['formule'],
            'date_reservation': reservation['date_reservation'],
            'heure_reservation': reservation['heure_reservation'],
            'nombre_personnes': reservation['nombre_personnes'],
            'message': reservation['message'],
            'statut': reservation['statut'],
            'date_creation': reservation['date_creation']
        })

    return jsonify(reservations_list)

@app.route('/api/reservations/<int:reservation_id>/status', methods=['PUT'])
def update_reservation_status(reservation_id):
    """Met à jour le statut d'une réservation et envoie un email si acceptée"""
    data = request.get_json()

    if 'statut' not in data:
        return jsonify({'error': 'Le champ statut est requis'}), 400

    try:
        # Récupérer les informations de la réservation avant mise à jour
        reservation = database.get_reservation_by_id(reservation_id)

        if not reservation:
            return jsonify({'error': 'Réservation non trouvée'}), 404

        # Mettre à jour le statut
        database.update_reservation_status(reservation_id, data['statut'])

        # Envoyer un email selon le nouveau statut
        email_sent = False
        try:
            if data['statut'] in ['acceptee', 'confirmee']:
                print(f"[INFO] Tentative d'envoi d'email de confirmation à {reservation['email']}")
                email_sent = email_service.send_confirmation_email(dict(reservation))
            elif data['statut'] in ['refusee', 'annulee']:
                print(f"[INFO] Tentative d'envoi d'email de refus à {reservation['email']}")
                email_sent = email_service.send_rejection_email(dict(reservation))
        except Exception as e:
            print(f"[ERROR] Exception lors de l'envoi d'email: {str(e)}")

        response_message = 'Statut mis à jour avec succès'
        if data['statut'] in ['acceptee', 'confirmee', 'refusee', 'annulee']:
            if email_sent:
                response_message += ' et email envoyé au client'
            else:
                response_message += ' (email non envoyé - vérifier la configuration SMTP)'

        return jsonify({
            'success': True,
            'message': response_message,
            'email_sent': email_sent
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
