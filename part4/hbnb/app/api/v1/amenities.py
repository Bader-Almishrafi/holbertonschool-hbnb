from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from hbnb.app.services import facade

api = Namespace('amenities', description='Amenity operations')
amenity_model = api.model('Amenity', {'name': fields.String(required=True)})


def amenity_to_response(amenity):
    return {'id': amenity.id, 'name': amenity.name}


@api.route('/')
class AmenityList(Resource):
    def get(self):
        return [amenity_to_response(a) for a in facade.get_all_amenities()], 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    def post(self):
        if not get_jwt().get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        try:
            amenity = facade.create_amenity(api.payload or {})
        except ValueError as e:
            return {'error': str(e)}, 400
        return amenity_to_response(amenity), 201


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity_to_response(amenity), 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    def put(self, amenity_id):
        if not get_jwt().get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        try:
            updated = facade.update_amenity(amenity_id, api.payload or {})
        except ValueError as e:
            return {'error': str(e)}, 400
        return amenity_to_response(updated), 200
