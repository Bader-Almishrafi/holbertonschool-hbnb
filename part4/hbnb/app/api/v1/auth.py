from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from hbnb.app.services import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

register_model = api.model('Register', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})


def user_payload(user):
    return {'user': user.to_dict()}


@api.route('/register')
class Register(Resource):
    @api.expect(register_model, validate=True)
    def post(self):
        try:
            user = facade.create_user(api.payload or {})
        except ValueError as e:
            return {'error': str(e)}, 400
        access_token = create_access_token(identity=str(user.id), additional_claims={'is_admin': user.is_admin})
        return {'access_token': access_token, **user_payload(user)}, 201


@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        credentials = api.payload or {}
        user = facade.get_user_by_email(credentials.get('email', ''))
        if not user or not user.verify_password(credentials.get('password', '')):
            return {'error': 'Invalid credentials'}, 401
        access_token = create_access_token(identity=str(user.id), additional_claims={'is_admin': user.is_admin})
        return {'access_token': access_token, **user_payload(user)}, 200


@api.route('/me')
class Me(Resource):
    @jwt_required()
    def get(self):
        user = facade.get_user(get_jwt_identity())
        if not user:
            return {'error': 'User not found'}, 404
        return {'is_admin': get_jwt().get('is_admin', False), **user_payload(user)}, 200
