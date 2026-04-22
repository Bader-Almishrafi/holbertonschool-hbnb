from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt
from hbnb.app.services import facade

api = Namespace('admin', description='Admin dashboard operations')


def admin_only():
    if not get_jwt().get('is_admin', False):
        return {'error': 'Admin privileges required'}, 403
    return None


@api.route('/stats')
class AdminStats(Resource):
    @jwt_required()
    def get(self):
        denied = admin_only()
        if denied:
            return denied
        return facade.get_admin_stats(), 200


@api.route('/users')
class AdminUsers(Resource):
    @jwt_required()
    def get(self):
        denied = admin_only()
        if denied:
            return denied
        return [u.to_dict() for u in facade.get_all_users()], 200


@api.route('/places')
class AdminPlaces(Resource):
    @jwt_required()
    def get(self):
        denied = admin_only()
        if denied:
            return denied
        return [p.to_dict() for p in facade.get_all_places()], 200


@api.route('/bookings')
class AdminBookings(Resource):
    @jwt_required()
    def get(self):
        denied = admin_only()
        if denied:
            return denied
        bookings = facade.get_all_bookings()
        return [{
            'id': b.id,
            'user_name': b.user.full_name if b.user else 'Unknown',
            'place_title': b.place.title if b.place else 'Unknown',
            'check_in_date': b.check_in_date.isoformat(),
            'check_out_date': b.check_out_date.isoformat(),
            'status': b.status,
            'total_price': float(b.total_price)
        } for b in bookings], 200
