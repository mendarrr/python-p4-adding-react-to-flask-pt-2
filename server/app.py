# server/app.py
#!/usr/bin/env python3
import logging
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Movie

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/movies', methods=['GET'])
def movies():
    try:
        if request.method == 'GET':
            movies = Movie.query.all()
            return make_response(
                jsonify([movie.to_dict() for movie in movies]),
                200,
            )
        return make_response(
            jsonify({"text": "Method Not Allowed"}),
            405,
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return make_response(jsonify({"error": str(e)}), 500)

if __name__ == '__main__':
    app.run(port=5555)
