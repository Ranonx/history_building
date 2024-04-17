#!/usr/bin/env python3

from flask import Flask, request, render_template
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy()
db.init_app(app)

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_ref = db.Column(db.String(120), unique=True, nullable=False)

def load_initialize_data():
    print("load_initialize_data executed")
    db.create_all()  # Ensure all tables are created
     # Open the JSON file and load its data
    with open("historic-building.json", 'r') as file:
        data = json.load(file)
        for feature in data["features"]:
            place = Place(file_ref=feature['properties']['FILE_REF'])
            db.session.add(place)
        db.session.commit()
        

@app.route('/')
def main():
     # Open the JSON file and load its data
    with open("historic-building.json", 'r') as file:
        geojson_data = json.load(file)
    # Pass the loaded data to the template
    return render_template('base.html', geojson_data=geojson_data)


if __name__ == '__main__':
    with app.app_context():
        load_initialize_data()
    app.run(debug=True)