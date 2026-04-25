from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from hbnb.app.services import facade

api = Namespace('reviews', description='Review operations')

review_create_model = api.model('ReviewCreate', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'place_id': fields.String(required=True)
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String,
    'rating': fields.Integer
})


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


@api.route('/')
class ReviewList(Resource):
    def get(self):
        return [review_to_response(review) for review in facade.get_all_reviews()], 200

    @jwt_required()
    @api.expect(review_create_model, validate=True)
    def post(self):
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)
        data = api.payload or {}
        place = facade.get_place(data.get('place_id'))
        if not place:
            return {'error': 'Place not found'}, 404
        if not is_admin and str(place.owner_id) == str(current_user_id):
            return {'error': 'You cannot review your own place.'}, 400
        for review in facade.get_reviews_by_place(place.id):
            if str(review.user_id) == str(current_user_id):
                return {'error': 'You have already reviewed this place.'}, 400
        try:
            new_review = facade.create_review({'text': data.get('text'), 'rating': data.get('rating'), 'place_id': data.get('place_id'), 'user_id': current_user_id})
        except ValueError as e:
            return {'error': str(e)}, 400
        return review_to_response(new_review), 201


@api.route('/<review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review_to_response(review), 200

    @jwt_required()
    @api.expect(review_update_model, validate=True)
    def put(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        current_user_id = get_jwt_identity()
        if not get_jwt().get('is_admin', False) and str(review.user_id) != str(current_user_id):
            return {'error': 'Unauthorized action'}, 403
        try:
            updated_review = facade.update_review(review_id, api.payload or {})
        except ValueError as e:
            return {'error': str(e)}, 400
        return review_to_response(updated_review), 200

    @jwt_required()
    def delete(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        current_user_id = get_jwt_identity()
        if not get_jwt().get('is_admin', False) and str(review.user_id) != str(current_user_id):
            return {'error': 'Unauthorized action'}, 403
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
