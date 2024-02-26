#!/usr/bin/python3
"""starting Flask Application"""

from os import getenv
from flask import Flask
from models import storage
from app.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """calls the close function"""
    return storage.close()


@app.errorhandler(404)
def error_handle(error):
    """handler for 404 errors that returns a JSON-formatted 404
    status code response"""
    return jsonify({"error": "Not Found"}), 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')), threaded=True)
