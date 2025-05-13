# server/app.py
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>Flask is working!</h1>'

@app.route('/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()
    return jsonify([{'id': pet.id, 'name': pet.name, 'species': pet.species} for pet in pets])

@app.route('/pets', methods=['POST'])
def create_pet():
    data = request.get_json()
    new_pet = Pet(name=data.get('name'), species=data.get('species'))
    db.session.add(new_pet)
    db.session.commit()
    return jsonify({'id': new_pet.id, 'name': new_pet.name, 'species': new_pet.species}), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)

