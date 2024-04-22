from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Place(db.Model):
    __tablename__ = 'place'
    id = db.Column(db.Integer, primary_key=True)
    district = db.Column(db.String(50), nullable=False)

class Visited(db.Model):
    __tablename__ = 'visited'
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    place = db.relationship('Place')

@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    total_places = Place.query.count()
    total_visits = Visited.query.count()
    visit_ratio = (total_visits / total_places * 100) if total_places > 0 else 0

    # Query to count visits per district
    district_counts = db.session.query(
        Place.district,
        func.count(Visited.id).label('visit_count')
    ).join(Visited, Visited.place_id == Place.id) \
      .group_by(Place.district) \
      .order_by(func.count(Visited.id).desc()) \
      .all()

    # Find the district with the highest visit count
    highest_district = district_counts[0] if district_counts else ('None', 0)

    return jsonify({
        'total_places': total_places,
        'total_visits': total_visits,
        'visit_ratio': round(visit_ratio, 2),  # rounding for cleanliness
        'visits_per_district': {district: count for district, count in district_counts},
        'highest_visit_district': highest_district[0],
        'highest_visit_count': highest_district[1]
    })

if __name__ == '__main__':
    app.run(port=5001, debug=True)
