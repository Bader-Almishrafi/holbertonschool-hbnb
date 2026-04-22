from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from hbnb.app.services import facade

api = Namespace('users', description='User operations')

user_create_model = api.model('UserCreate', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'is_admin': fields.Boolean(default=False)
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String,
    'last_name': fields.String,
    'password': fields.String
})


@api.route('/')
class UserList(Resource):
    def get(self):
        return [user.to_dict() for user in facade.get_all_users()], 200

    @api.expect(user_create_model, validate=True)
    def post(self):
        data = request.get_json() or {}
        auth_header = request.headers.get('Authorization', '')
        is_admin_request = bool(data.get('is_admin'))
        if is_admin_request and not auth_header:
            return {'error': 'Admin privileges required to create admin users'}, 403
        try:
            user = facade.create_user({
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'email': data.get('email'),
                'password': data.get('password'),
                'is_admin': bool(data.get('is_admin')) if auth_header else False
            })
        except ValueError as e:
            return {'error': str(e)}, 400
        return user.to_dict(), 201


@api.route('/<string:user_id>')
class UserResource(Resource):
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    def put(self, user_id):
        target = facade.get_user(user_id)
        if not target:
            return {'error': 'User not found'}, 404
        claims = get_jwt()
        requester_id = get_jwt_identity()
        if not claims.get('is_admin') and requester_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        data = request.get_json() or {}
        data.pop('email', None)
        data.pop('is_admin', None)
        try:
            updated = facade.update_user(user_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return updated.to_dict(), 200
