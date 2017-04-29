from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)


@app.route('/')
def index():
    return jsonify({'web': 'js'})


if __name__ == '__main__':
    app.run(debug=True)
