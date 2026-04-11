from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from hbnb.app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


def amenity_to_response(amenity):
    return {
        'id': amenity.id,
        'name': amenity.name
    }


@api.route('/')
class AmenityList(Resource):
    @api.response(200, 'Amenities retrieved successfully')
    def get(self):
        """Retrieve all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity_to_response(a) for a in amenities], 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(403, 'Admin privileges required')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = api.payload or {}

        try:
            amenity = facade.create_amenity(data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return amenity_to_response(amenity), 201


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity_to_response(amenity), 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity successfully updated')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin privileges required')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        data = api.payload or {}

        try:
            updated = facade.update_amenity(amenity_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return amenity_to_response(updated), 200