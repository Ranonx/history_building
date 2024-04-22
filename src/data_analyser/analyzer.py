from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app)  # This is especially useful if you're accessing this service from another domain.

class Place(db.Model):
    __tablename__ = 'place'
    id = db.Column(db.Integer, primary_key=True)

class Visited(db.Model):
    __tablename__ = 'visited'
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))

@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    total_places = Place.query.count()
    total_visits = Visited.query.count()
    if total_places > 0:
        visit_ratio = (total_visits / total_places) * 100
    else:
        visit_ratio = 0  # Avoid division by zero if no places are defined.

    return jsonify({
        'total_places': total_places,
        'total_visits': total_visits,
        'visit_ratio': visit_ratio
    })

if __name__ == '__main__':
    app.run(port=5001, debug=True)
