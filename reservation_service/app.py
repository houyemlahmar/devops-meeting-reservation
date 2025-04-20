from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaConsumer
import json
import threading

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db-reservation:5432/reservations'
db = SQLAlchemy(app)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120))
    salle_id = db.Column(db.Integer)
    date = db.Column(db.String(50))

@app.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.get_json()
    reservation = Reservation(user_email=data['user_email'], salle_id=data['salle_id'], date=data['date'])
    db.session.add(reservation)
    db.session.commit()
    return jsonify({'message': 'Réservation créée'}), 201

@app.route('/reservations', methods=['GET'])
def get_reservations():
    reservations = Reservation.query.all()
    return jsonify([
        {'id': r.id, 'user_email': r.user_email, 'salle_id': r.salle_id, 'date': r.date}
        for r in reservations
    ])

def consume_events():
    consumer = KafkaConsumer(
        'user-events',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    for message in consumer:
        print(f"[Kafka] Event reçu: {message.value}")

threading.Thread(target=consume_events).start()

app.run(host="0.0.0.0", port=5000)
