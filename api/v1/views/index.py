#!/usr/bin/python3
"""
a file index.py

"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def show_status():
    """show status"""
    status = {
            'status': 'ok'
            }
    return jsonify(status)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def show_stats():
    """show stats"""
    stats = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'users': storage.count('User')
            }

    return jsonify(stats)
