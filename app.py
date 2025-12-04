# app.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import config
import os
app = Flask(__name__)


app.config.from_object(config)
app.config['UPLOAD_FOLDER'] = config.BASE_STORAGE
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)

from models import *
from routes import *


def validar_token():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return False
    token = auth_header.split("Bearer ")[-1]
    return token == config.API_TOKEN


@app.before_request
def before_request():
    if request.method == "OPTIONS":
        return '', 200
    if request.endpoint in ['download', 'home']:
        return
    if not validar_token():
        return jsonify({"error": "Unauthorized"}), 401


# app.py (Línea 38 en adelante)

if __name__ == '__main__':
    with app.app_context():
        pass

    app.run(debug=True, port=5001)