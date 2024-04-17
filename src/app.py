#!/usr/bin/env python3

from flask import Flask, request, render_template,json
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

app = Flask(__name__)


@app.route('/')
def main():
     # Open the JSON file and load its data
    with open("historic-building.json", 'r') as file:
        geojson_data = json.load(file)
    # Pass the loaded data to the template
    return render_template('base.html', geojson_data=geojson_data)

def load_initialize_data():
    db.create_all()  # Ensure all tables are created


if __name__ == '__main__':
    app.run(debug=True)