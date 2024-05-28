#!/usr/bin/python3
"""
Review object that handles all default RESTFul API actions

"""
from api.v1.views import app_views
from models import storage
from models.review import Review
from flask import jsonify, abort, request


url = '/places/<place_id>/reviews'


@app_views.route(url, methods=['GET'], strict_slashes=False)
def get_place_review(place_id):
    """
    method to retrieve the list of all review objects
    """

    _list = []
    all_objs = storage.all('Review')
    for obj in all_objs.values():
        if obj.place_id == place_id:
            _list.append(obj.to_dict())
    response = jsonify(_list)
    response.status_code = 200
    return response


@app_views.route(url, methods=['POST'], strict_slashes=False)
def add_review(place_id):
    """
    Creates a review object
    """
    us_json = request.get_json(silent=False)
    if us_json is None:
        abort(400, 'Not a JSON')
    if storage.get('Place', place_id) is None:
        abort(404)
    if 'user_id' not in us_json:
        abort(400, 'Missing user_id')
    user = storage.get('User', us_json['user_id'])
    if user is None:
        abort(404)
    if 'text' not in us_json:
        abort(400, 'Missing text')
    new_Review = Review(**us_json)
    new_Review.save()
    response = jsonify(new_Review.to_dict())
    response.status_code = 201
    return response


url = '/reviews/<review_id>'


@app_views.route(url, methods=['GET'], strict_slashes=False)
def get_review_id(review_id):
    """
    Retrieves a review object by id

    """
    us_obj = storage.get('Review', str(review_id))
    if us_obj is None:
        abort(404)
    response = jsonify(us_obj.to_dict())
    response.status_code = 200
    return response


@app_views.route(url, methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    """
    Delete a review object

    """
    us_obj = storage.get('Review', str(review_id))
    if us_obj is None:
        abort(404)
    us_obj.delete()
    storage.save()
    response = jsonify({})
    response.status_code = 200
    return response


@app_views.route(url, methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a review object

    """
    us_obj = storage.get('Review', str(review_id))
    if us_obj is None:
        abort(404)
    us_json = request.get_json(silent=True)
    if us_json is None:
        abort(400, 'Not a JSON')
    for key, value in us_json.items():
        if key not in ['id', 'user_id', 'created_at', 'updated_at']:
            setattr(us_obj, key, value)
    storage.save()
    response = jsonify(us_obj.to_dict())
    response.status_code = 200
    return response
