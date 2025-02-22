#!/usr/bin/python3
"""
AirBnB_clone_v3 application api
"""
import os
from flask import Flask, jsonify, Response
from flask_cors import CORS
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown():
    '''To handle teardown'''
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    ''' Handles errors'''
    status = {'error': 'Not found'}
    return jsonify(status), 404


if __name__ == '__main__':
    try:
        host = os.environ.get('HBNB_API_HOST')
    except Exception:
        host = '0.0.0.0'
    try:
        port = os.environ.get('HBNB_API_PORT')
    except Exception:
        port = '5000'

    app.run(host=host, port=port, threaded=True)
