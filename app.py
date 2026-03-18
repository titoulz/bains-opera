from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import database
import email_service_resend as email_service
import auth
import json
from datetime import datetime
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"], "allow_headers": ["Content-Type", "Authorization"]}})

# Initialiser la base de données au démarrage
database.init_db()

@app.route('/')
def index():
    return "API de réservation - Les Bains de l'Opéra"

# Routes pour servir les fichiers HTML et autres fichiers statiques
@app.route('/<path:path>')
def serve_static(path):
    """Sert les fichiers HTML, CSS, JS et images"""
    if os.path.exists(path):
        return send_from_directory('.', path)
    return "Fichier non trouvé", 404

# Route de connexion
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authentifie un administrateur"""
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username et password requis'}), 400

    if auth.authenticate_user(username, password):
        token = auth.generate_token(username)
        return jsonify({
            'success': True,
            'token': token,
            'message': 'Connexion réussie'
        })
    else:
        return jsonify({'error': 'Identifiants incorrects'}), 401

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
@auth.token_required
def get_reservations(current_user):
    """Récupère toutes les réservations (protégé)"""
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
@auth.token_required
def update_reservation_status(current_user, reservation_id):
    """Met à jour le statut d'une réservation et envoie un email si acceptée (protégé)"""
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

# ============================================
# Endpoints CMS - Gestion du contenu
# ============================================

# Paramètres du site
@app.route('/api/cms/settings', methods=['GET'])
def get_settings():
    """Récupère tous les paramètres du site"""
    try:
        settings = database.get_all_settings()
        return jsonify(settings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cms/settings', methods=['PUT'])
@auth.token_required
def update_settings(current_user):
    """Met à jour les paramètres du site (protégé)"""
    data = request.get_json()

    try:
        for key, value in data.items():
            database.update_setting(key, value)
        return jsonify({'success': True, 'message': 'Paramètres mis à jour avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Images du carousel
@app.route('/api/cms/carousel', methods=['GET'])
def get_carousel():
    """Récupère les images du carousel actives"""
    try:
        images = database.get_carousel_images()
        return jsonify(images)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cms/carousel/all', methods=['GET'])
@auth.token_required
def get_all_carousel(current_user):
    """Récupère toutes les images du carousel (protégé)"""
    try:
        images = database.get_all_carousel_images()
        return jsonify(images)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cms/carousel', methods=['POST'])
@auth.token_required
def create_carousel(current_user):
    """Crée une nouvelle image de carousel (protégé)"""
    data = request.get_json()

    required = ['image_url', 'title', 'subtitle']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Le champ {field} est requis'}), 400

    try:
        image_id = database.create_carousel_image(
            data['image_url'],
            data['title'],
            data['subtitle'],
            data.get('button_text', ''),
            data.get('button_link', ''),
            data.get('display_order', 0)
        )
        return jsonify({'success': True, 'id': image_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cms/carousel/<int:image_id>', methods=['PUT'])
@auth.token_required
def update_carousel(current_user, image_id):
    """Met à jour une image de carousel (protégé)"""
    data = request.get_json()

    try:
        database.update_carousel_image(
            image_id,
            image_url=data.get('image_url'),
            title=data.get('title'),
            subtitle=data.get('subtitle'),
            button_text=data.get('button_text'),
            button_link=data.get('button_link'),
            display_order=data.get('display_order'),
            active=data.get('active')
        )
        return jsonify({'success': True, 'message': 'Image mise à jour avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cms/carousel/<int:image_id>', methods=['DELETE'])
@auth.token_required
def delete_carousel(current_user, image_id):
    """Supprime une image de carousel (protégé)"""
    try:
        database.delete_carousel_image(image_id)
        return jsonify({'success': True, 'message': 'Image supprimée avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Sections de contenu
@app.route('/api/cms/content', methods=['GET'])
def get_content():
    """Récupère les sections de contenu"""
    page = request.args.get('page')
    try:
        sections = database.get_all_content_sections(page)
        return jsonify(sections)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cms/content/<page>/<section_key>', methods=['GET'])
def get_content_section(page, section_key):
    """Récupère une section de contenu spécifique"""
    try:
        section = database.get_content_section(page, section_key)
        if section:
            return jsonify(section)
        return jsonify({'error': 'Section non trouvée'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cms/content', methods=['PUT'])
@auth.token_required
def update_content(current_user):
    """Met à jour une section de contenu (protégé)"""
    data = request.get_json()

    required = ['page', 'section_key']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Le champ {field} est requis'}), 400

    try:
        database.update_content_section(
            data['page'],
            data['section_key'],
            title=data.get('title'),
            content=data.get('content')
        )
        return jsonify({'success': True, 'message': 'Contenu mis à jour avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Offres spéciales
@app.route('/api/cms/offers', methods=['GET'])
def get_offers():
    """Récupère les offres spéciales actives"""
    try:
        offers = database.get_special_offers(active_only=True)
        return jsonify(offers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cms/offers/all', methods=['GET'])
@auth.token_required
def get_all_offers(current_user):
    """Récupère toutes les offres spéciales (protégé)"""
    try:
        offers = database.get_special_offers(active_only=False)
        return jsonify(offers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cms/offers', methods=['POST'])
@auth.token_required
def create_offer(current_user):
    """Crée une nouvelle offre spéciale (protégé)"""
    data = request.get_json()

    required = ['title', 'description']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Le champ {field} est requis'}), 400

    try:
        offer_id = database.create_special_offer(
            data['title'],
            data['description'],
            price=data.get('price'),
            old_price=data.get('old_price'),
            valid_from=data.get('valid_from'),
            valid_until=data.get('valid_until')
        )
        return jsonify({'success': True, 'id': offer_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cms/offers/<int:offer_id>', methods=['PUT'])
@auth.token_required
def update_offer(current_user, offer_id):
    """Met à jour une offre spéciale (protégé)"""
    data = request.get_json()

    try:
        database.update_special_offer(
            offer_id,
            title=data.get('title'),
            description=data.get('description'),
            price=data.get('price'),
            old_price=data.get('old_price'),
            valid_from=data.get('valid_from'),
            valid_until=data.get('valid_until'),
            active=data.get('active')
        )
        return jsonify({'success': True, 'message': 'Offre mise à jour avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cms/offers/<int:offer_id>', methods=['DELETE'])
@auth.token_required
def delete_offer(current_user, offer_id):
    """Supprime une offre spéciale (protégé)"""
    try:
        database.delete_special_offer(offer_id)
        return jsonify({'success': True, 'message': 'Offre supprimée avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Gestion des formules
@app.route('/api/cms/formules', methods=['GET'])
@auth.token_required
def get_all_formules_admin(current_user):
    """Récupère toutes les formules (protégé)"""
    try:
        formules = database.get_all_formules()
        return jsonify(formules)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cms/formules', methods=['POST'])
@auth.token_required
def create_formule_admin(current_user):
    """Crée une nouvelle formule (protégé)"""
    data = request.get_json()

    required = ['nom', 'type', 'description', 'prix', 'duree']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Le champ {field} est requis'}), 400

    try:
        formule_id = database.create_formule(
            data['nom'],
            data['type'],
            data['description'],
            data['prix'],
            data['duree']
        )
        return jsonify({'success': True, 'id': formule_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cms/formules/<int:formule_id>', methods=['PUT'])
@auth.token_required
def update_formule_admin(current_user, formule_id):
    """Met à jour une formule (protégé)"""
    data = request.get_json()

    try:
        database.update_formule(
            formule_id,
            nom=data.get('nom'),
            type_formule=data.get('type'),
            description=data.get('description'),
            prix=data.get('prix'),
            duree=data.get('duree')
        )
        return jsonify({'success': True, 'message': 'Formule mise à jour avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cms/formules/<int:formule_id>', methods=['DELETE'])
@auth.token_required
def delete_formule_admin(current_user, formule_id):
    """Supprime une formule (protégé)"""
    try:
        database.delete_formule(formule_id)
        return jsonify({'success': True, 'message': 'Formule supprimée avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
