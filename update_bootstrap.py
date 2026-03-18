#!/usr/bin/env python3
"""
Script pour ajouter Bootstrap à toutes les pages HTML
"""
import os
import re

# Liste des fichiers HTML à mettre à jour
html_files = [
    'hammam.html', 'massages.html', 'soins.html', 'nos-escales.html',
    'escales-spa.html', 'escales-enveloppement.html', 'tarifs.html',
    'infos.html', 'reservation.html', 'admin.html', 'login.html'
]

bootstrap_css = '    <!-- Bootstrap CSS -->\n    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">'
bootstrap_js = '\n    <!-- Bootstrap JS -->\n    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>'

# Nouveau navbar Bootstrap
new_navbar = '''    <header>
        <nav class="navbar navbar-expand-lg navbar-light bg-white sticky-top shadow-sm">
            <div class="container-fluid px-lg-5">
                <a class="navbar-brand logo" href="index.html">Les Bains de l'Opéra</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="index.html">Accueil</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="hammam.html">Hammam</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="massages.html">Massages</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="soins.html">Soins Visage</a>
                        </li>
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                Nos Escales
                            </a>
                            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                                <li><a class="dropdown-item" href="nos-escales.html">Nos Escales</a></li>
                                <li><a class="dropdown-item" href="escales-spa.html">Nos Escales avec SPA</a></li>
                                <li><a class="dropdown-item" href="escales-enveloppement.html">Nos Escales avec Enveloppement</a></li>
                            </ul>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="tarifs.html">Offres Spéciales</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="infos.html">Infos Pratiques</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>'''

for filename in html_files:
    if not os.path.exists(filename):
        print(f"Fichier {filename} non trouvé, skip...")
        continue

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Ajouter Bootstrap CSS si pas déjà présent
    if 'bootstrap' not in content.lower():
        # Ajouter Bootstrap CSS avant styles.css
        content = re.sub(
            r'(\s*<link rel="stylesheet" href="styles\.css">)',
            f'{bootstrap_css}\n\\1',
            content
        )

        # Ajouter Bootstrap JS avant </body>
        content = re.sub(
            r'(\s*</body>)',
            f'{bootstrap_js}\\1',
            content
        )
        print(f"✓ Bootstrap ajouté à {filename}")

    # Remplacer l'ancien navbar par le nouveau (Bootstrap)
    # Pattern pour trouver l'ancien header/nav
    old_nav_pattern = r'<header>.*?</header>'
    if re.search(old_nav_pattern, content, re.DOTALL):
        content = re.sub(old_nav_pattern, new_navbar, content, flags=re.DOTALL)
        print(f"✓ Navbar mis à jour dans {filename}")

    # Sauvegarder le fichier modifié
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("\n✅ Mise à jour terminée!")
