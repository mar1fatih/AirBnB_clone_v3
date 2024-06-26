#!/usr/bin/python3
"""
Place object that handles all default RESTFul API actions

"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from flask import jsonify, abort, request


url = '/cities/<city_id>/places'


@app_views.route(url, methods=['GET'], strict_slashes=False)
def get_city_place(city_id):
    """
    method to retrieve the list of all Place objects
    """

    _list = []
    if storage.get('City', city_id) is None:
        abort(404)
    all_objs = storage.all('Place')
    for obj in all_objs.values():
        if obj.city_id == city_id:
            _list.append(obj.to_dict())
    response = jsonify(_list)
    response.status_code = 200
    return response


@app_views.route(url, methods=['POST'], strict_slashes=False)
def add_place(city_id):
    """
    Creates a place object
    """
    us_json = request.get_json(silent=False)
    if storage.get('City', city_id) is None:
        abort(404)
    if us_json is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in us_json:
        abort(400, 'Missing user_id')
    user = storage.get('User', us_json['user_id'])
    if user is None:
        abort(404)
    if 'name' not in us_json:
        abort(400, 'Missing name')
    us_json['city_id'] = city_id
    new_place = Place(**us_json)
    new_place.save()
    response = jsonify(new_place.to_dict())
    response.status_code = 201
    return response


url = '/places/<place_id>'


@app_views.route(url, methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    """
    Retrieves a Place object by id

    """
    us_obj = storage.get('Place', str(place_id))
    if us_obj is None:
        abort(404)
    response = jsonify(us_obj.to_dict())
    response.status_code = 200
    return response


@app_views.route(url, methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
    """
    Delete a place object

    """
    us_obj = storage.get('Place', str(place_id))
    if us_obj is None:
        abort(404)
    us_obj.delete()
    storage.save()
    response = jsonify({})
    response.status_code = 200
    return response


@app_views.route(url, methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object

    """
    us_obj = storage.get('Place', str(place_id))
    if us_obj is None:
        abort(404)
    us_json = request.get_json(silent=True)
    if us_json is None:
        abort(400, 'Not a JSON')
    for key, value in us_json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(us_obj, key, value)
    storage.save()
    response = jsonify(us_obj.to_dict())
    response.status_code = 200
    return response


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """
    Retrieves a list of all Place objects depending of the JSON in the body
    of the request
    """

    us_json = request.get_json(silent=True)
    if us_json is None:
        abort(400, 'Not a JSON')
    _list = []
    all_objs = storage.all('Place')
    if us_json:
        for obj in all_objs.values():
            if all(key in obj.to_dict().values() for key in us_json.values()):
                _list.append(obj.to_dict())
        response = jsonify(_list)
        response.status_code = 200
        return response
    else:
        abort(400, 'Not a JSON')