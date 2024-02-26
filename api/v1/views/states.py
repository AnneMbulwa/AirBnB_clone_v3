#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """retrieve list of State using GET"""
    states = storage.all(State).values()
    x_state = [state.to_dict() for state in states]
    return jsonify(x_state)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """If the state_id is not linked to any State object, raise a 404 error"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """deleting a State object"""
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_get():
    """creating State with POST"""
    if not request.get_json():
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in request.get_json():
        return abort(400, {'message': 'Missing name'})

    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update State method is PUT"""
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return abort(400, {'message': 'Not a JSON'})

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
