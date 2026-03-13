from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from hbnb.app.services import facade

api = Namespace('places', description='Place operations')

place_create_model = api.model('PlaceCreate', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=False, description='List of amenity IDs')
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(required=False, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=False, description='Price per night'),
    'latitude': fields.Float(required=False, description='Latitude of the place'),
    'longitude': fields.Float(required=False, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=False, description='List of amenity IDs')
})


def place_to_response(place):
    return {
        'id': place.id,
        'title': place.title,
        'description': place.description,
        'price': place.price,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'owner_id': place.owner.id if getattr(place, 'owner', None) else None,
        'amenities': [amenity.id for amenity in getattr(place, 'amenities', [])]
    }


@api.route('/')
class PlaceList(Resource):
    @api.response(200, 'Places retrieved successfully')
    def get(self):
        """Retrieve all places (public)"""
        places = facade.get_all_places()
        return [place_to_response(place) for place in places], 200

    @jwt_required()
    @api.expect(place_create_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place for the authenticated user"""
        current_user_id = get_jwt_identity()
        data = api.payload or {}

        place_data = {
            'title': data.get('title'),
            'description': data.get('description', ''),
            'price': data.get('price'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'owner_id': current_user_id,
            'amenities': data.get('amenities', [])
        }

        try:
            new_place = facade.create_place(place_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return place_to_response(new_place), 201


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID (public)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place_to_response(place), 200

    @jwt_required()
    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place only if the authenticated user is the owner"""
        current_user_id = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        if not getattr(place, 'owner', None) or str(place.owner.id) != str(current_user_id):
            return {'error': 'Unauthorized action'}, 403

        data = api.payload or {}

        if 'owner_id' in data:
            data.pop('owner_id')

        try:
            updated_place = facade.update_place(place_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return place_to_response(updated_place), 200