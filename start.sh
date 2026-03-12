#!/bin/bash

# Script de démarrage pour Les Bains de l'Opéra
echo "=== Les Bains de l'Opéra - Système de Réservation ==="
echo ""

# Vérifier si les dépendances sont installées
if ! python3 -c "import flask" &> /dev/null; then
    echo "Installation des dépendances..."
    pip3 install -r requirements.txt
fi

# Vérifier si la base de données existe
if [ ! -f "reservations.db" ]; then
    echo "Initialisation de la base de données..."
    python3 database.py
fi

echo ""
echo "Démarrage des serveurs..."
echo ""
echo "Frontend: http://localhost:8000"
echo "API Backend: http://localhost:5000"
echo "Page de réservation: http://localhost:8000/reservation.html"
echo "Interface admin: http://localhost:8000/admin.html"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter les serveurs"
echo ""

# Démarrer Flask en arrière-plan
python3 app.py &
FLASK_PID=$!

# Démarrer le serveur HTTP
python3 -m http.server 8000

# Arrêter Flask à la fin
kill $FLASK_PID
