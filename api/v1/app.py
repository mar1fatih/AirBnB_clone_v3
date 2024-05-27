#!/usr/bin/python3
'''module of api app'''
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    '''teardown the session'''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''handler for 404 errors'''
    err = {

        'error': 'Not found'
    }
    return make_response(jsonify(err), 404)


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = 5000
    app.run(host=host, port=port, threaded=True)
