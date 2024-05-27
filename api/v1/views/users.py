#!/usr/bin/python3
"""
User object that handles all default RESTFul API actions
"""
from models.user import User
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user():
    """
    method to retrieve the list of all user objects
    """
    _list = []
    all_objs = storage.all('User')
    for obj in all_objs.values():
        _list.append(obj.to_dict())
    response = jsonify(_list)
    response.status_code = 200
    return response


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """
    Creates an User object
    """
    us_json = request.get_json(silent=False)
    if us_json is None:
        abort(400, 'Not a JSON')
    if 'email' not in us_json:
        abort(400, 'Missing email')
    if 'password' not in us_json:
        abort(400, 'Missing password')
    new_user = User(**us_json)
    new_user.save()
    response = jsonify(new_user.to_dict())
    response.status_code = 201
    return response


url = '/users/<user_id>'


@app_views.route(url, methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """
    Retrieves an User object by id
    """
    us_obj = storage.get('User', str(user_id))
    if us_obj is None:
        abort(404)
    response = jsonify(us_obj.to_dict())
    response.status_code = 200
    return response


@app_views.route(url, methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """
    Delete an User object
    """
    us_obj = storage.get('User', str(user_id))
    if us_obj is None:
        abort(404)
    us_obj.delete()
    storage.save()
    response = jsonify({})
    response.status_code = 200
    return response


@app_views.route(url, methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates an User object
    """
    us_obj = storage.get('User', str(user_id))
    if us_obj is None:
        abort(404)
    us_json = request.get_json(silent=True)
    if us_json is None:
        abort(400, 'Not a JSON')
    for key, value in us_json.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(us_obj, key, value)
    storage.save()
    response = jsonify(us_obj.to_dict())
    response.status_code = 200
    return response
