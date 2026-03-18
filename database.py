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

    # Table des sections de contenu (pour le CMS)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content_sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page TEXT NOT NULL,
            section_key TEXT NOT NULL,
            title TEXT,
            content TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(page, section_key)
        )
    ''')

    # Table des paramètres du site
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS site_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key TEXT NOT NULL UNIQUE,
            setting_value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table des images du carousel
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS carousel_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_url TEXT NOT NULL,
            title TEXT,
            subtitle TEXT,
            button_text TEXT,
            button_link TEXT,
            display_order INTEGER DEFAULT 0,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table des offres spéciales
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS special_offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price REAL,
            old_price REAL,
            valid_from DATE,
            valid_until DATE,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    # Initialiser les paramètres du site si vide
    cursor.execute('SELECT COUNT(*) FROM site_settings')
    if cursor.fetchone()[0] == 0:
        site_settings = [
            # Informations générales
            ('site_name', 'Les Bains de l\'Opéra'),
            ('site_description', 'Le plus grand hammam traditionnel au cœur de Lyon'),
            ('address', '20 Rue Joseph Serlin, 69001 Lyon'),
            ('phone', ''),
            ('email', 'contact@bainsopera.com'),

            # Horaires
            ('hours_lundi', 'Fermé'),
            ('hours_mardi', 'Fermé'),
            ('hours_mercredi', '11h - 21h'),
            ('hours_jeudi', '11h - 19h'),
            ('hours_vendredi', '11h - 22h'),
            ('hours_samedi', '11h - 19h'),
            ('hours_dimanche', 'Fermé'),

            # Footer
            ('footer_about', 'Les Bains de l\'Opéra est votre destination bien-être au cœur de Lyon. Hammam traditionnel, massages et soins dans un cadre raffiné depuis plus de 25 ans.'),

            # Thème et couleurs
            ('theme_primary_color', '#D4915E'),
            ('theme_secondary_color', '#2C2C2C'),
            ('theme_accent_color', '#C67D4E'),
            ('theme_background_color', '#F5F5F5'),
            ('theme_text_color', '#333333'),
            ('theme_light_bg_color', '#FFF9F5'),

            # Typographie
            ('theme_font_family', 'Arial, sans-serif'),
            ('theme_heading_font', 'Georgia, serif'),

            # Textes personnalisables
            ('home_hero_title', 'LES BAINS DE L\'OPÉRA'),
            ('home_hero_subtitle', 'Le plus grand hammam traditionnel au cœur de Lyon'),
            ('home_intro_title', 'Bienvenue aux Bains de l\'Opéra'),
            ('home_intro_text', 'Depuis 25 ans, Les Bains de l\'Opéra est le plus grand hammam traditionnel en plein cœur de Lyon avec ses 500 m² dédiés au bien-être et à la beauté.'),
            ('cta_section_title', 'Offrez-vous un moment d\'exception'),
            ('cta_section_subtitle', 'Réservez dès maintenant votre escale bien-être'),

            # Boutons
            ('btn_primary_text', 'Réserver'),
            ('btn_secondary_text', 'En savoir plus'),
        ]
        cursor.executemany('INSERT INTO site_settings (setting_key, setting_value) VALUES (?, ?)', site_settings)
        conn.commit()

    # Initialiser les images du carousel si vide
    cursor.execute('SELECT COUNT(*) FROM carousel_images')
    if cursor.fetchone()[0] == 0:
        carousel_images = [
            ('images/accueil.avif', 'LES BAINS DE L\'OPÉRA', 'Le plus grand hammam traditionnel au cœur de Lyon', 'Réserver', 'reservation.html', 1, 1),
            ('images/massage2.avif', 'MASSAGES & SOINS', 'Découvrez nos rituels de bien-être', 'Nos Massages', 'massages.html', 2, 1),
            ('images/lavabo2.avif', 'UN LIEU D\'EXCEPTION', 'Au cœur du premier arrondissement de Lyon', 'En savoir plus', 'infos.html', 3, 1),
            ('images/lavabo.avif', 'HAMMAM TRADITIONNEL', 'Réservé aux femmes - Un espace de détente unique', 'Découvrir', 'hammam.html', 4, 1),
        ]
        cursor.executemany('''
            INSERT INTO carousel_images (image_url, title, subtitle, button_text, button_link, display_order, active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', carousel_images)
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

# ============================================
# Fonctions CMS - Gestion du contenu
# ============================================

def get_all_settings():
    """Récupère tous les paramètres du site"""
    conn = sqlite3.connect('reservations.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM site_settings')
    settings = cursor.fetchall()
    conn.close()
    return {row['setting_key']: row['setting_value'] for row in settings}

def update_setting(setting_key, setting_value):
    """Met à jour ou crée un paramètre du site"""
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO site_settings (setting_key, setting_value, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(setting_key) DO UPDATE SET
            setting_value = excluded.setting_value,
            updated_at = CURRENT_TIMESTAMP
    ''', (setting_key, setting_value))
    conn.commit()
    conn.close()

def get_carousel_images():
    """Récupère toutes les images du carousel actives"""
    conn = sqlite3.connect('reservations.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM carousel_images WHERE active = 1 ORDER BY display_order')
    images = cursor.fetchall()
    conn.close()
    return [dict(row) for row in images]

def get_all_carousel_images():
    """Récupère toutes les images du carousel (incluant inactives)"""
    conn = sqlite3.connect('reservations.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM carousel_images ORDER BY display_order')
    images = cursor.fetchall()
    conn.close()
    return [dict(row) for row in images]

def create_carousel_image(image_url, title, subtitle, button_text, button_link, display_order=0):
    """Crée une nouvelle image de carousel"""
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO carousel_images (image_url, title, subtitle, button_text, button_link, display_order)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (image_url, title, subtitle, button_text, button_link, display_order))
    image_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return image_id

def update_carousel_image(image_id, image_url=None, title=None, subtitle=None, button_text=None, button_link=None, display_order=None, active=None):
    """Met à jour une image de carousel"""
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()

    updates = []
    params = []

    if image_url is not None:
        updates.append('image_url = ?')
        params.append(image_url)
    if title is not None:
        updates.append('title = ?')
        params.append(title)
    if subtitle is not None:
        updates.append('subtitle = ?')
        params.append(subtitle)
    if button_text is not None:
        updates.append('button_text = ?')
        params.append(button_text)
    if button_link is not None:
        updates.append('button_link = ?')
        params.append(button_link)
    if display_order is not None:
        updates.append('display_order = ?')
        params.append(display_order)
    if active is not None:
        updates.append('active = ?')
        params.append(active)

    params.append(image_id)

    if updates:
        cursor.execute(f'''
            UPDATE carousel_images
            SET {', '.join(updates)}
            WHERE id = ?
        ''', params)

    conn.commit()
    conn.close()

def delete_carousel_image(image_id):
    """Supprime une image du carousel"""
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM carousel_images WHERE id = ?', (image_id,))
    conn.commit()
    conn.close()

def get_content_section(page, section_key):
    """Récupère une section de contenu"""
    conn = sqlite3.connect('reservations.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM content_sections WHERE page = ? AND section_key = ?', (page, section_key))
    section = cursor.fetchone()
    conn.close()
    return dict(section) if section else None

def get_all_content_sections(page=None):
    """Récupère toutes les sections de contenu d'une page ou toutes les pages"""
    conn = sqlite3.connect('reservations.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if page:
        cursor.execute('SELECT * FROM content_sections WHERE page = ?', (page,))
    else:
        cursor.execute('SELECT * FROM content_sections')
    sections = cursor.fetchall()
    conn.close()
    return [dict(row) for row in sections]

def update_content_section(page, section_key, title=None, content=None):
    """Met à jour ou crée une section de contenu"""
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO content_sections (page, section_key, title, content, updated_at)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(page, section_key) DO UPDATE SET
            title = COALESCE(excluded.title, title),
            content = COALESCE(excluded.content, content),
            updated_at = CURRENT_TIMESTAMP
    ''', (page, section_key, title, content))
    conn.commit()
    conn.close()

def get_special_offers(active_only=True):
    """Récupère les offres spéciales"""
    conn = sqlite3.connect('reservations.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if active_only:
        cursor.execute('''
            SELECT * FROM special_offers
            WHERE active = 1
            AND (valid_from IS NULL OR valid_from <= DATE('now'))
            AND (valid_until IS NULL OR valid_until >= DATE('now'))
            ORDER BY created_at DESC
        ''')
    else:
        cursor.execute('SELECT * FROM special_offers ORDER BY created_at DESC')

    offers = cursor.fetchall()
    conn.close()
    return [dict(row) for row in offers]

def create_special_offer(title, description, price=None, old_price=None, valid_from=None, valid_until=None):
    """Crée une nouvelle offre spéciale"""
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO special_offers (title, description, price, old_price, valid_from, valid_until)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, description, price, old_price, valid_from, valid_until))
    offer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return offer_id

def update_special_offer(offer_id, title=None, description=None, price=None, old_price=None, valid_from=None, valid_until=None, active=None):
    """Met à jour une offre spéciale"""
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()

    updates = []
    params = []

    if title is not None:
        updates.append('title = ?')
        params.append(title)
    if description is not None:
        updates.append('description = ?')
        params.append(description)
    if price is not None:
        updates.append('price = ?')
        params.append(price)
    if old_price is not None:
        updates.append('old_price = ?')
        params.append(old_price)
    if valid_from is not None:
        updates.append('valid_from = ?')
        params.append(valid_from)
    if valid_until is not None:
        updates.append('valid_until = ?')
        params.append(valid_until)
    if active is not None:
        updates.append('active = ?')
        params.append(active)

    params.append(offer_id)

    if updates:
        cursor.execute(f'''
            UPDATE special_offers
            SET {', '.join(updates)}
            WHERE id = ?
        ''', params)

    conn.commit()
    conn.close()

def delete_special_offer(offer_id):
    """Supprime une offre spéciale"""
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM special_offers WHERE id = ?', (offer_id,))
    conn.commit()
    conn.close()

def update_formule(formule_id, nom=None, type_formule=None, description=None, prix=None, duree=None):
    """Met à jour une formule existante"""
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()

    updates = []
    params = []

    if nom is not None:
        updates.append('nom = ?')
        params.append(nom)
    if type_formule is not None:
        updates.append('type = ?')
        params.append(type_formule)
    if description is not None:
        updates.append('description = ?')
        params.append(description)
    if prix is not None:
        updates.append('prix = ?')
        params.append(prix)
    if duree is not None:
        updates.append('duree = ?')
        params.append(duree)

    params.append(formule_id)

    if updates:
        cursor.execute(f'''
            UPDATE formules
            SET {', '.join(updates)}
            WHERE id = ?
        ''', params)

    conn.commit()
    conn.close()

def create_formule(nom, type_formule, description, prix, duree):
    """Crée une nouvelle formule"""
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO formules (nom, type, description, prix, duree)
        VALUES (?, ?, ?, ?, ?)
    ''', (nom, type_formule, description, prix, duree))
    formule_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return formule_id

def delete_formule(formule_id):
    """Supprime une formule"""
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM formules WHERE id = ?', (formule_id,))
    conn.commit()
    conn.close()

def get_all_formules():
    """Récupère toutes les formules"""
    conn = sqlite3.connect('reservations.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM formules ORDER BY type, nom')
    formules = cursor.fetchall()
    conn.close()
    return [dict(row) for row in formules]

if __name__ == '__main__':
    init_db()
