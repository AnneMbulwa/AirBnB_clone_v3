#!/usr/bin/python3
"""Create a new view for User object that handles all default RESTFul
API actions:"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects: GET"""
    x_user = storage.all(User).values()
    users = [user.to_dict() for user in x_user]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """Retrieve a User object by id with method get"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    return jsonify(users.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete an User object by its id with method delete"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Insert a new User object with method post"""
    if not request.get_json():
        return abort(400, {'message': 'Not a JSON'})
    if 'email' not in body:
        return abort(400, {'message': 'Missing email'})
    if 'password' not in body:
        return abort(400, {'message': 'Missing password'})
    y_user = User(**request.get_json())
    y_user.save()
    return jsonify(y_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user_id(user_id):
    """Update an User object with method put"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return abort(400, {'message': 'Not a JSON'})
    for key, value in request.get_json().items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
