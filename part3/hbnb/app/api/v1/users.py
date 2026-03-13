from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from hbnb.app.services import facade

api = Namespace('users', description='User operations')

user_create_model = api.model('UserCreate', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user')
})


def user_to_response(user):
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }


@api.route('/')
class UserList(Resource):
    @api.expect(user_create_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_user.id,
            'message': 'User created successfully'
        }, 201

    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """Retrieve a list of users"""
        users = facade.get_all_users()
        return [user_to_response(u) for u in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user_to_response(user), 200

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, user_id):
        """Update authenticated user's own profile (excluding email/password)"""
        current_user_id = get_jwt_identity()

        if current_user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = api.payload or {}

        if 'email' in data or 'password' in data:
            return {'error': 'You cannot modify email or password'}, 400

        try:
            updated = facade.update_user(user_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            "message": "User updated successfully",
            "user": user_to_response(updated)
        }, 200