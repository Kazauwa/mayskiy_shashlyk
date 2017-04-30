import os, json

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)


@app.route('/api/')
def api_index():
    site_root_dir = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(site_root_dir, "static", "google.json")
    with open(json_url) as fire_data:
        data = json.load(fire_data)
    return json.dumps(data)

@app.route('/api/add_event')
def api_add_event():
    return 'Ok', 200


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
