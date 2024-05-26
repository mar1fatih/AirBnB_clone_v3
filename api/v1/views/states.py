#!/usr/bin/python3
"""
State objects that handles all default RESTFul API actions

"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """
    Retrieves the list of all State objects

    """
    _list = []
    objs = storage.all('State')
    for key in objs.keys():
        _list.append(objs[key].to_dict())
    return jsonify(_list)


id_url = '/states/<string:state_id>'


@app_views.route(id_url, methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """
    Retrieves State object by id
    """
    obj = storage.get('State', state_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route(id_url, methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """
    Deletes a State object

    """
    obj = storage.get('State', state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    create new state obj
    """
    st_json = request.get_json(silent=True)
    if st_json is None:
        abort(400, 'Not a JSON')
    if 'name' not in st_json:
        abort(400, 'Missing name')

    new_st = State(**st_json)
    new_st.save()
    response = jsonify(new_st.to_dict())
    response.status_code = 201
    return response


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def modify_state(state_id):
    """
    updates state object by id
    """
    st_json = request.get_json(silent=True)
    if st_json is None:
        abort(400, 'Not a JSON')
    obj = storage.get("State", str(state_id))
    if obj is None:
        abort(404)
    for key, value in st_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict())
