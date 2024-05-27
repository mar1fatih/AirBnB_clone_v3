#!/usr/bin/python3
"""
State objects that handles all default RESTFul API actions

"""
import os
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.state import State
from flask import jsonify, abort, request


url = "/places/<place_id>/amenities"

@app_views.route(url, methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieves the list of all amenities objects
    under a place object

    """
    if storage.get('Place', place_id) is None:
        abort(404)
    place_obj = storage.get('Place', place_id)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = place_obj.amenities
    else:
        amenities = place_obj.amenity_ids
    _list = []
    for obj in amenities:
        _list.append(obj.to_dict())
    return jsonify(_list)



id_url = '/places/<place_id>/amenities/<amenity_id>'


@app_views.route(id_url, methods=['DELETE'], strict_slashes=False)
def del_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object from a Place relationship

    """
    if storage.get('Place', place_id) is None:
        abort(404)
    if storage.get('Amenity', amenity_id) is None:
        abort(404)
    amenity_obj = storage.get('Amenity', amenity_id)
    place_obj = storage.get('Place', place_id)
    if amenity_obj.place_id != place_id:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_obj.amenities.remove(amenity_obj)
    else:
        place_obj.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route(id_url, methods=["POST"], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """
    Link a Amenity object to a Place object
    """
    if storage.get('Place', place_id) is None:
        abort(404)
    if storage.get('Amenity', amenity_id) is None:
        abort(404)
    amenity_obj = storage.get('Amenity', amenity_id)
    place_obj = storage.get('Place', place_id)
    if amenity_obj.place_id == place_id:
        return jsonify(amenity_obj.to_dict()), 200
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_obj.amenities.append(amenity_obj)
    else:
        place_obj.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity_obj.to_dict()), 201
