from flask import Flask, jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """Retrieves the list of all Review objects of a Place: GET method"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object with GET method"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete review object with delete method"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """create a review object with post method"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    x_data = request.get_json()
    if 'user_id' not in x_data:
        abort(400, "Missing user_id")
    if 'text' not in x_data:
        abort(400, "Missing text")

    user_id = x_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    x_review = Review(place_id=place_id, **x_data)
    x_review.save()
    return jsonify(x_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        cont = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        if key not in cont:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
