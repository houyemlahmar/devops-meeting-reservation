from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaProducer
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db-user:5432/users'
db = SQLAlchemy(app)

producer = KafkaProducer(bootstrap_servers='kafka:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(50))

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(email=data['email'], name=data['name'])
    db.session.add(user)
    db.session.commit()

    producer.send('user-events', {'event': 'user_created', 'email': user.email})
    return jsonify({'message': 'User created'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'email': u.email, 'name': u.name} for u in users])

app.run(host="0.0.0.0", port=5000)
