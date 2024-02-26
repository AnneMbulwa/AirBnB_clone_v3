#!/usr/bin/python3
"""Create a new view for Amenity objects that handles
all default RESTFul API actions"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """Get all Amenities"""
    amenities = storage.all(Amenity).values()
    x_amenity = [
        amenity.to_dict() for amenity in amenities]
    return jsonify(x_amenity)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """Get Amenity filter by id
    If the amenity_id is not linked to any Amenity object, raise a 404 error
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an Amenity with method delete"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def insert_amenity():
    """Insert new Amenity using method post"""
    if not request.get_json():
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in request.get_json():
        return abort(400, {'message': 'Missing name'})
    x_amenity = Amenity(**request.get_json())
    x_amenity.save()
    return jsonify(x_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity_id(amenity_id):
    """Update an Amenity with method put"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return abort(400, {'message': 'Not a JSON'})
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
