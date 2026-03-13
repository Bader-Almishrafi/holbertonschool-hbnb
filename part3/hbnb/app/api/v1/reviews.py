from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from hbnb.app.services import facade

api = Namespace('reviews', description='Review operations')

review_create_model = api.model('ReviewCreate', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Review rating'),
    'place_id': fields.String(required=True, description='Place ID')
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=False, description='Review text'),
    'rating': fields.Integer(required=False, description='Review rating')
})


def review_to_response(review):
    return {
        'id': review.id,
        'text': review.text,
        'rating': review.rating,
        'user_id': review.user.id if getattr(review, 'user', None) else None,
        'place_id': review.place.id if getattr(review, 'place', None) else None
    }


@api.route('/')
class ReviewList(Resource):
    @api.response(200, 'Reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return [review_to_response(review) for review in reviews], 200

    @jwt_required()
    @api.expect(review_create_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a review.
        - Regular user: cannot review own place, cannot review same place twice
        - Admin: can bypass ownership restriction, but duplicate review still blocked
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        data = api.payload or {}

        place = facade.get_place(data.get('place_id'))
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin:
            if getattr(place, 'owner', None) and str(place.owner.id) == str(current_user_id):
                return {'error': 'You cannot review your own place.'}, 400

        existing_reviews = facade.get_reviews_by_place(place.id)
        if existing_reviews is None:
            existing_reviews = []

        for review in existing_reviews:
            if getattr(review, 'user', None) and str(review.user.id) == str(current_user_id):
                return {'error': 'You have already reviewed this place.'}, 400

        review_data = {
            'text': data.get('text'),
            'rating': data.get('rating'),
            'place_id': data.get('place_id'),
            'user_id': current_user_id
        }

        try:
            new_review = facade.create_review(review_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return review_to_response(new_review), 201


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review_to_response(review), 200

    @jwt_required()
    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review successfully updated')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review; admin bypasses ownership restriction"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin:
            if not getattr(review, 'user', None) or str(review.user.id) != str(current_user_id):
                return {'error': 'Unauthorized action'}, 403

        data = api.payload or {}
        if 'user_id' in data:
            data.pop('user_id')
        if 'place_id' in data:
            data.pop('place_id')

        try:
            updated_review = facade.update_review(review_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return review_to_response(updated_review), 200

    @jwt_required()
    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review; admin bypasses ownership restriction"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin:
            if not getattr(review, 'user', None) or str(review.user.id) != str(current_user_id):
                return {'error': 'Unauthorized action'}, 403

        deleted = facade.delete_review(review_id)
        if not deleted:
            return {'error': 'Review not found'}, 404

        return {'message': 'Review deleted successfully'}, 200