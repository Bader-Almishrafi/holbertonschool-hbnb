# part2/hbnb/app/api/v1/users.py
from flask_restx import Namespace, Resource, fields
from hbnb.app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})


def user_to_response(user):
    """Return user dict without sensitive fields (password not included)."""
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
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
            # validation errors from model
            return {'error': str(e)}, 400

        return user_to_response(new_user), 201

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

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = api.payload

        if data.get('email') and data['email'].strip().lower() != user.email.strip().lower():
            existing_user = facade.get_user_by_email(data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

        try:
            updated = facade.update_user(user_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {"message": "User updated successfully", "user": user_to_response(updated)}, 200
