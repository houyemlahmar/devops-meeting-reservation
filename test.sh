#!/bin/bash

echo "📦 Création de l'utilisateur"
curl -X POST http://localhost:30001/users -H "Content-Type: application/json" -d '{"name": "Alice", "email": "alice@example.com"}'
echo -e "\n📦 Création de la salle"
curl -X POST http://localhost:30002/salles -H "Content-Type: application/json" -d '{"name": "Salle A", "capacity": 20}'
echo -e "\n📦 Création de la réservation"
curl -X POST http://localhost:30003/reservations -H "Content-Type: application/json" -d '{"user_id": 1, "salle_id": 1, "date": "2025-04-25", "heure_debut": "09:00", "heure_fin": "10:00"}'
echo -e "\n📄 Résultat final des réservations :"
curl http://localhost:30003/reservations
