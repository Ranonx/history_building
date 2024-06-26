#!/usr/bin/env python3

from flask import Flask, request, render_template, jsonify
import json
import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS  # Import CORS
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes
PrometheusMetrics(app)  # Automatically exposes endpoint at /metrics

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy()
db.init_app(app)

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_ref = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    grade = db.Column(db.String(20),nullable=False)
    district=db.Column(db.String(20),nullable=False)
    address=db.Column(db.String(120),nullable=False)

class Visited(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    visit_date = db.Column(db.DateTime, default=datetime.utcnow)
    place = db.relationship('Place', backref='visits')

def load_initialize_data():
    print("load_initialize_data executed")
    db.create_all()  # Ensure all tables are created
     # Open the JSON file and load its data
    if Place.query.first() is None:  # Check if the places table is empty
        with open("historic-building.json", 'r') as file:
            data = json.load(file)
            for feature in data["features"]:
                place = Place(file_ref=feature['properties']['FILE_REF'], 
                              name=feature['properties']['NAME'], 
                              grade=feature['properties']['GRADE'],
                              district=feature['properties']['DISTRICT'],
                              address=feature['properties']['ADDRESS'])
                db.session.add(place)
            db.session.commit()
        

@app.route('/')
def home():
     # Open the JSON file and load its data
    with open("historic-building.json", 'r') as file:
        geojson_data = json.load(file)
    # Pass the loaded data to the template
    return render_template('base.html', geojson_data=geojson_data,current_page='home')

@app.route('/stats')
def recent_visits():
    recent_visits = db.session.query(
        Visited.visit_date, 
        Place.name, 
        Place.district, 
        Place.address
    ).join(Place, Visited.place_id == Place.id) \
    .order_by(Visited.visit_date.desc()) \
    .limit(10).all()
        
    # Fetch statistics data from the data analyzer service
    stats_response = requests.get('http://localhost:5001/fetch-data')
    if stats_response.status_code == 200:
        stats_data = stats_response.json()
    else:
        stats_data = {'total_places': 0, 'total_visits': 0, 'visit_ratio': 0}
    return render_template('table.html', visits=recent_visits, stats=stats_data, current_page='stats')


@app.route('/add-visit', methods=['POST'])
def add_visit():
    # Ensure the request content type is JSON
    if not request.is_json:
        return jsonify({'error': 'Invalid content type, expected application/json'}), 400
    
    data = request.get_json()
    file_ref = data.get('place_id')
    if not file_ref:
        return jsonify({'error': 'place_id is required'}), 400
    place = Place.query.filter_by(file_ref=file_ref).first()
    if not place:
        return jsonify({'error': 'Place not found'}), 404

     # Check if a visit to this place already exists
    existing_visit = Visited.query.filter_by(place_id=place.id).first()
    if existing_visit:
        return jsonify({'error': 'Visit already recorded'}), 409  # 409 Conflict

    visited = Visited(place_id=place.id)
    db.session.add(visited)
    db.session.commit()
    return jsonify({'message': 'Visit added successfully'}), 201

@app.route('/get-place-details')
def get_place_details():
    file_ref = request.args.get('file_ref')
    place = Place.query.filter_by(file_ref=file_ref).first()
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    
    visited = Visited.query.filter_by(place_id=place.id).first() is not None
    return jsonify({
        'name': place.name,
        'address': place.address,
        'visited': visited  # True or False
    })

if __name__ == '__main__':
    with app.app_context():
        load_initialize_data()
    app.run(debug=True)