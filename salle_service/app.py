from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db-salle:5432/salles'
db = SQLAlchemy(app)

class Salle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    capacite = db.Column(db.Integer)

@app.route('/salles', methods=['POST'])
def create_salle():
    data = request.get_json()
    salle = Salle(nom=data['nom'], capacite=data['capacite'])
    db.session.add(salle)
    db.session.commit()
    return jsonify({'message': 'Salle créée'}), 201

@app.route('/salles', methods=['GET'])
def get_salles():
    salles = Salle.query.all()
    return jsonify([{'id': s.id, 'nom': s.nom, 'capacite': s.capacite} for s in salles])

app.run(host="0.0.0.0", port=5000)
