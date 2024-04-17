#!/usr/bin/env python3

from flask import Flask, request, render_template,json

app = Flask(__name__)


@app.route('/')
def main():
     # Open the JSON file and load its data
    with open("historic-building.json", 'r') as file:
        geojson_data = json.load(file)
    # Pass the loaded data to the template
    return render_template('base.html', geojson_data=geojson_data)

if __name__ == '__main__':
    app.run(debug=True)