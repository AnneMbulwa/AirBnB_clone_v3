#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions"""

from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id):
    """retrieve list of City using method GET"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    0x_city = [city.to_dict() for city in states.cities]
    return jsonify(x_city)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """If the city_id is not linked to any City object, raise a 404 error"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(city_id):
    """deleting a city object"""
    if city_id is None:
        abort(404)
    citx = storage.get(City, city_id)
    if citx is None:
        abort(404)
    storage.delete(citx)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creating City with method POST"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in request.get_json():
        return abort(400, {'message': 'Missing name'})

    city = City(**request.get_json())
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update City method is PUT"""
    if city_id is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return abort(400, {'message': 'Not a JSON'})

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
