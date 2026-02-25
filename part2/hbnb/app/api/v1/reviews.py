from flask_restx import Namespace, Resource, fields
from hbnb.app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


def review_full(r):
    return {
        "id": r.id,
        "text": r.text,
        "rating": r.rating,
        "user_id": r.user.id if r.user else None,
        "place_id": r.place.id if r.place else None
    }


def review_compact(r):
    return {"id": r.id, "text": r.text, "rating": r.rating}


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            new_review = facade.create_review(api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400
        return review_full(new_review), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [review_compact(r) for r in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        r = facade.get_review(review_id)
        if not r:
            return {"error": "Review not found"}, 404
        return review_full(r), 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        r = facade.get_review(review_id)
        if not r:
            return {"error": "Review not found"}, 404

        try:
            updated_review = facade.update_review(review_id, api.payload)  # updates text/rating only
        except ValueError as e:
            return {"error": str(e)}, 400

        return {"message": "Review updated successfully", "review": review_full(updated_review)}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        ok = facade.delete_review(review_id)
        if not ok:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200