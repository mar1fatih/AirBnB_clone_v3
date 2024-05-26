#!/usr/bin/python3
"""
api app 

"""
from flask import Flask, make_response, jsonify
import models
from api.v1.views import app_views
from os import getenv


HBNB_API_HOST = getenv('HBNB_API_HOST')
HBNB_API_PORT = getenv('HBNB_API_PORT')

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exception):
    """teardown the session"""
    models.storage.close()

@app.errorhandler(404)
def not_found(error):
    """
    handler for 404 errors

    """
    err = {

    'error': 'Not found'
            
    }
    return make_response(jsonify(err), 404)


if __name__ == '__main__':
    if models.storage_t == 'db':
        app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
    else:
        app.run(host='0.0.0.0', port='5000', threaded=True)
