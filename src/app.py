#!/usr/bin/env python3

from flask import Flask, request, render_template, jsonify
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
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
def main():
     # Open the JSON file and load its data
    with open("historic-building.json", 'r') as file:
        geojson_data = json.load(file)
    # Pass the loaded data to the template
    return render_template('base.html', geojson_data=geojson_data)

@app.route('/get-place-details')
def get_place_details():
    file_ref = request.args.get('file_ref')
    place = Place.query.filter_by(file_ref=file_ref).first_or_404()
    return jsonify(name=place.name, address=place.address)

if __name__ == '__main__':
    with app.app_context():
        load_initialize_data()
    app.run(debug=True)