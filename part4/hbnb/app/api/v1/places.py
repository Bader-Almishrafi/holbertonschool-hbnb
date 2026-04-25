from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from hbnb.app.services import facade

api = Namespace('places', description='Place operations')

place_create_model = api.model('PlaceCreate', {
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'city': fields.String,
    'country': fields.String,
    'max_guests': fields.Integer,
    'image_url': fields.String,
    'amenities': fields.List(fields.String)
})

place_update_model = api.inherit('PlaceUpdate', place_create_model, {})


def review_to_response(review):
    return {
        'id': review.id,
        'text': review.text,
        'rating': review.rating,
        'user_id': review.user_id,
        'user_name': review.user.full_name if review.user else 'Unknown',
        'place_id': review.place_id,
        'created_at': review.created_at.isoformat() if review.created_at else None
    }


def place_to_response(place):
    payload = place.to_dict()
    payload['owner_name'] = place.owner.full_name if place.owner else 'Unknown host'
    payload['amenities'] = [{'id': amenity.id, 'name': amenity.name} for amenity in place.amenities]
    payload['reviews'] = [review_to_response(review) for review in sorted(place.reviews, key=lambda x: x.created_at, reverse=True)]
    payload['bookings_count'] = len(place.bookings)
    return payload


@api.route('/')
class PlaceList(Resource):
    def get(self):
        city = request.args.get('city')
        max_price = request.args.get('max_price', type=float)
        q = request.args.get('q')
        return [place_to_response(place) for place in facade.get_all_places(city=city, max_price=max_price, q=q)], 200

    @jwt_required()
    @api.expect(place_create_model, validate=True)
    def post(self):
        data = api.payload or {}
        try:
            new_place = facade.create_place({
                'title': data.get('title'),
                'description': data.get('description', ''),
                'price': data.get('price'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'city': data.get('city', 'Riyadh'),
                'country': data.get('country', 'Saudi Arabia'),
                'max_guests': data.get('max_guests', 2),
                'image_url': data.get('image_url'),
                'owner_id': get_jwt_identity(),
                'amenities': data.get('amenities', [])
            })
        except ValueError as e:
            return {'error': str(e)}, 400
        return place_to_response(new_place), 201


@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place_to_response(place), 200

    @jwt_required()
    @api.expect(place_update_model, validate=True)
    def put(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)
        if not is_admin and str(place.owner_id) != str(current_user_id):
            return {'error': 'Unauthorized action'}, 403
        data = api.payload or {}
        try:
            updated_place = facade.update_place(place_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return place_to_response(updated_place), 200

    @jwt_required()
    def delete(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)
        if not is_admin and str(place.owner_id) != str(current_user_id):
            return {'error': 'Unauthorized action'}, 403
        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200


@api.route('/<place_id>/reviews')
class PlaceReviews(Resource):
    def get(self, place_id):
        if not facade.get_place(place_id):
            return {'error': 'Place not found'}, 404
        return [review_to_response(review) for review in facade.get_reviews_by_place(place_id)], 200
