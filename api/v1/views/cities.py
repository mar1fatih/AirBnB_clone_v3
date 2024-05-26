#!/usr/bin/python3
"""
City objects that handles all default RESTFul API actions
"""
from models.city import City
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views

url = 'states/<state_id>/cities'


@app_views.route(url, methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """
    method to retrieve the list of all City objects
    """
    _list = []
    st_obj = storage.get("State", str(state_id))

    if st_obj is None:
        abort(404)
    for ct_obj in st_obj.cities:
        _list.append(ct_obj.to_dict())
    return jsonify(_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_by_city_id(city_id):
    """
    Retrieves a City object by city id
    """
    ct_obj = storage.get("City", str(city_id))
    if ct_obj is None:
        abort(404)
    return jsonify(ct_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """
    delete a City object by city id
    """
    ct_obj = storage.get("City", str(city_id))
    if ct_obj is None:
        abort(404)
    storage.delete(ct_obj)
    storage.save()
    data = jsonify({})
    data.status_code = 200
    return data


url = '/states/<state_id>/cities'


@app_views.route(url, methods=['POST'], strict_slashes=False)
def add_city(state_id):
    """
    add new city using POST method
    """
    ct_json = request.get_json(silent=True)
    if ct_json is None:
        abort(400, 'Not a JSON')

    obj = storage.get("State", str(state_id))
    if not obj:
        abort(404)
    if 'name' not in ct_json:
        abort(400, 'Missing name')

    ct_json["state_id"] = state_id
    new_city = City(**ct_json)
    new_city.save()
    response = jsonify(new_city.to_dict())
    response.status_code = 201
    return response


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    update city infos
    """
    ct_json = request.get_json(silent=True)
    if ct_json is None:
        abort(400, 'Not a JSON')

    obj = storage.get("City", str(city_id))
    if not obj:
        abort(404)
    for key, value in ct_json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    response = jsonify(obj.to_dict())
    response.status_code = 200
    return response
