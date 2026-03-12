import sqlite3
from datetime import datetime

def init_db():
    """Initialise la base de données avec les tables nécessaires"""
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()

    # Table des réservations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT NOT NULL,
            telephone TEXT NOT NULL,
            formule TEXT NOT NULL,
            date_reservation DATE NOT NULL,
            heure_reservation TIME NOT NULL,
            nombre_personnes INTEGER DEFAULT 1,
            message TEXT,
            statut TEXT DEFAULT 'en_attente',
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table des formules disponibles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS formules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT,
            prix REAL NOT NULL,
            duree INTEGER
        )
    ''')

    # Table des créneaux horaires
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS creneaux (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jour_semaine TEXT NOT NULL,
            heure_debut TIME NOT NULL,
            heure_fin TIME NOT NULL,
            actif BOOLEAN DEFAULT 1
        )
    ''')

    conn.commit()

    # Insérer les formules si la table est vide
    cursor.execute('SELECT COUNT(*) FROM formules')
    if cursor.fetchone()[0] == 0:
        formules = [
            # Nos Escales
            ('MALTE', 'escale', 'Hammam + gommage corps', 35, 90),
            ('CRÈTE', 'escale', 'Hammam + gommage corps + massage 15 minutes', 45, 105),
            ('RHODES', 'escale', 'Hammam + gommage corps + massage 30 minutes', 60, 120),
            ('SICILE', 'escale', 'Hammam + gommage corps + massage suédois 15 minutes', 50, 105),
            ('CHYPRE', 'escale', 'Hammam + gommage corps + massage 45 minutes', 80, 135),
            ('CORSE', 'escale', 'Hammam + gommage corps + massage suédois 30 minutes', 75, 120),

            # Escales avec SPA
            ('OMAN', 'escale_spa', 'Hammam + gommage corps + jacuzzi 15 minutes', 60, 105),
            ('EGÉE', 'escale_spa', 'Hammam + gommage corps + jacuzzi 15 minutes + massage 15 minutes', 70, 120),
            ('BALÉARES', 'escale_spa', 'Hammam + gommage corps + enveloppement au rhassoul + jacuzzi 15 minutes + massage 15 minutes', 85, 150),
            ('SUÉDOISE', 'escale_spa', 'Hammam + gommage corps + jacuzzi 15 minutes + massage suédois 15 minutes', 80, 120),
            ('JAVA', 'escale_spa', 'Hammam + gommage corps + jacuzzi 15 minutes + massage 30 minutes', 90, 135),
            ('BALTIQUE', 'escale_spa', 'Hammam + gommage corps + enveloppement au rhassoul + jacuzzi 15 minutes + massage 30 minutes + soin visage', 135, 210),

            # Hammam seul
            ('HAMMAM', 'hammam', 'Accès au hammam traditionnel', 25, 60),

            # Massages
            ('MASSAGE 15MIN', 'massage', 'Massage relaxant 15 minutes', 25, 15),
            ('MASSAGE 30MIN', 'massage', 'Massage relaxant 30 minutes', 45, 30),
            ('MASSAGE 45MIN', 'massage', 'Massage relaxant 45 minutes', 65, 45),
            ('MASSAGE 60MIN', 'massage', 'Massage relaxant 60 minutes', 85, 60),
            ('MASSAGE SUÉDOIS 30MIN', 'massage', 'Massage suédois 30 minutes', 55, 30),
            ('MASSAGE SUÉDOIS 60MIN', 'massage', 'Massage suédois 60 minutes', 95, 60),
        ]

        cursor.executemany('''
            INSERT INTO formules (nom, type, description, prix, duree)
            VALUES (?, ?, ?, ?, ?)
        ''', formules)

        conn.commit()

    # Insérer les créneaux horaires si la table est vide
    cursor.execute('SELECT COUNT(*) FROM creneaux')
    if cursor.fetchone()[0] == 0:
        creneaux = [
            ('Mercredi', '11:00', '21:00', 1),
            ('Jeudi', '11:00', '19:00', 1),
            ('Vendredi', '11:00', '22:00', 1),
            ('Samedi', '11:00', '19:00', 1),
        ]

        cursor.executemany('''
            INSERT INTO creneaux (jour_semaine, heure_debut, heure_fin, actif)
            VALUES (?, ?, ?, ?)
        ''', creneaux)

        conn.commit()

    conn.close()
    print("Base de données initialisée avec succès!")

def get_formules_by_type(type_formule=None):
    """Récupère les formules par type"""
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()

    if type_formule:
        cursor.execute('SELECT * FROM formules WHERE type = ?', (type_formule,))
    else:
        cursor.execute('SELECT * FROM formules')

    formules = cursor.fetchall()
    conn.close()
    return formules

def create_reservation(nom, prenom, email, telephone, formule, date_reservation, heure_reservation, nombre_personnes=1, message=''):
    """Crée une nouvelle réservation"""
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO reservations
        (nom, prenom, email, telephone, formule, date_reservation, heure_reservation, nombre_personnes, message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nom, prenom, email, telephone, formule, date_reservation, heure_reservation, nombre_personnes, message))

    reservation_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return reservation_id

def get_all_reservations():
    """Récupère toutes les réservations"""
    conn = sqlite3.connect('reservations.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM reservations
        ORDER BY date_reservation DESC, heure_reservation DESC
    ''')

    reservations = cursor.fetchall()
    conn.close()
    return reservations

def get_reservation_by_id(reservation_id):
    """Récupère une réservation par son ID"""
    conn = sqlite3.connect('reservations.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM reservations WHERE id = ?', (reservation_id,))
    reservation = cursor.fetchone()
    conn.close()

    return reservation

def update_reservation_status(reservation_id, statut):
    """Met à jour le statut d'une réservation"""
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE reservations
        SET statut = ?
        WHERE id = ?
    ''', (statut, reservation_id))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
