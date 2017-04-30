from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from models import Polygon, SpotM2MPolygon, FireSpot

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)


@app.route('/api/')
def api_index():
    response = []
    for polygon in Polygon.query.all():
        polygon_json = {}
        all_relations = SpotM2MPolygon.query.filter_by(polygon_id=polygon.id)
        all_spots = [FireSpot.query.get(relation.spot_id) for relation in all_relations]
        if not all_spots:
            continue
        polygon_json['type'] = polygon.type
        surface = [{'lat': spot.latitude, 'lng': spot.longitude} for spot in all_spots]
        polygon_json['external_surface'] = surface
        polygon_json['internal_surface'] = []
        response.append(polygon_json)
    return jsonify(response)


@app.route('/api/add_event')
def api_add_event():
    return 'Ok', 200


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
