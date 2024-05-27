#!/usr/bin/python3
"""
Amenity objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects
    """
    _list = []
    am_objs = storage.all('Amenity')
    for obj in am_objs.values():
        _list.append(obj.to_dict())
    response = jsonify(_list)
    response.status_code = 200
    return response


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity():
    """
    Creates an Amenity object
    """
    am_json = request.get_json(silent=True)
    if am_json is None:
        abort(400, 'Not a JSON')
    if 'name' not in am_json:
        abort(400, 'Missing name')
    new_am = Amenity(**am_json)
    new_am.save()
    response = jsonify(new_am.to_dict())
    response.status_code = 201
    return response


url = '/amenities/<amenity_id>'


@app_views.route(url, methods=['GET'], strict_slashes=False)
def get_am_id(amenity_id):
    """
    Retrieves an Amenity object by id
    """
    am_obj = storage.get('Amenity', str(amenity_id))
    if am_obj is None:
        abort(404)
    response = jsonify(am_obj.to_dict())
    response.status_code = 200
    return response


@app_views.route(url, methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
    """
    Deletes an Amenity object by id
    """
    am_obj = storage.get('Amenity', str(amenity_id))
    if am_obj is None:
        abort(404)
    storage.delete(am_obj)
    storage.save()
    response = jsonify({})
    response.status_code = 200
    return response


@app_views.route(url, methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates an Amenity object by id
    """
    am_obj = storage.get('Amenity', str(amenity_id))
    if am_obj is None:
        abort(404)
    am_json = request.get_json(silent=True)
    if am_json is None:
        abort(400, 'Not a JSON')
    for key, value in am_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(am_obj, key, value)
    am_obj.save()
    response = jsonify(am_obj.to_dict())
    response.status_code = 200
    return response
