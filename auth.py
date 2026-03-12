import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import hashlib

# Configuration
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'change-this-secret-key-in-production')
TOKEN_EXPIRATION_HOURS = 24

# Identifiants admin (à stocker en variable d'environnement en production)
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
# Hash SHA256 du mot de passe (à configurer en variable d'environnement)
ADMIN_PASSWORD_HASH = os.getenv('ADMIN_PASSWORD_HASH', hashlib.sha256('admin123'.encode()).hexdigest())

def hash_password(password):
    """Hash un mot de passe avec SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Vérifie qu'un mot de passe correspond au hash"""
    return hash_password(password) == password_hash

def generate_token(username):
    """Génère un token JWT"""
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    """Vérifie et décode un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Décorateur pour protéger les routes qui nécessitent une authentification"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Récupérer le token depuis les headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Format: "Bearer TOKEN"
            except IndexError:
                return jsonify({'error': 'Format de token invalide'}), 401

        if not token:
            return jsonify({'error': 'Token manquant'}), 401

        # Vérifier le token
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Token invalide ou expiré'}), 401

        # Passer les informations de l'utilisateur à la route
        return f(current_user=payload, *args, **kwargs)

    return decorated

def authenticate_user(username, password):
    """Authentifie un utilisateur"""
    if username == ADMIN_USERNAME and verify_password(password, ADMIN_PASSWORD_HASH):
        return True
    return False
