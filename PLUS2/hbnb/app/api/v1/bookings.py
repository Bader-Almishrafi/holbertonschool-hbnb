from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from hbnb.app.services import facade

api = Namespace('bookings', description='Booking operations')

booking_model = api.model('BookingCreate', {
    'place_id': fields.String(required=True),
    'check_in_date': fields.String(required=True, description='YYYY-MM-DD'),
    'check_out_date': fields.String(required=True, description='YYYY-MM-DD'),
    'guests': fields.Integer(required=False, default=1)
})

booking_update_model = api.model('BookingUpdate', {
    'check_in_date': fields.String,
    'check_out_date': fields.String,
    'guests': fields.Integer,
    'status': fields.String(description='pending / confirmed / cancelled')
})


def booking_to_response(booking):
    return {
        'id': booking.id,
        'user_id': booking.user_id,
        'user_name': booking.user.full_name if booking.user else 'Unknown',
        'place_id': booking.place_id,
        'place_title': booking.place.title if booking.place else 'Unknown place',
        'check_in_date': booking.check_in_date.isoformat(),
        'check_out_date': booking.check_out_date.isoformat(),
        'total_price': float(booking.total_price),
        'status': booking.status,
        'guests': booking.guests,
        'created_at': booking.created_at.isoformat() if booking.created_at else None
    }


@api.route('/')
class BookingList(Resource):
    @jwt_required()
    def get(self):
        is_admin = get_jwt().get('is_admin', False)
        user_id = None if is_admin else get_jwt_identity()
        status = None if not is_admin else None
        return [booking_to_response(b) for b in facade.get_all_bookings(user_id=user_id, status=status)], 200

    @jwt_required()
    @api.expect(booking_model, validate=True)
    def post(self):
        try:
            booking = facade.create_booking({**(api.payload or {}), 'user_id': get_jwt_identity()})
        except ValueError as e:
            return {'error': str(e)}, 400
        return booking_to_response(booking), 201


@api.route('/my-bookings')
class MyBookingList(Resource):
    @jwt_required()
    def get(self):
        return [booking_to_response(b) for b in facade.get_all_bookings(user_id=get_jwt_identity())], 200


@api.route('/<booking_id>')
class BookingResource(Resource):
    @jwt_required()
    def get(self, booking_id):
        booking = facade.get_booking(booking_id)
        if not booking:
            return {'error': 'Booking not found'}, 404
        current_user = get_jwt_identity()
        if not get_jwt().get('is_admin', False) and booking.user_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        return booking_to_response(booking), 200

    @jwt_required()
    @api.expect(booking_update_model, validate=True)
    def put(self, booking_id):
        booking = facade.get_booking(booking_id)
        if not booking:
            return {'error': 'Booking not found'}, 404
        current_user = get_jwt_identity()
        if not get_jwt().get('is_admin', False) and booking.user_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        try:
            updated = facade.update_booking(booking_id, api.payload or {})
        except ValueError as e:
            return {'error': str(e)}, 400
        return booking_to_response(updated), 200

    @jwt_required()
    def delete(self, booking_id):
        booking = facade.get_booking(booking_id)
        if not booking:
            return {'error': 'Booking not found'}, 404
        current_user = get_jwt_identity()
        if not get_jwt().get('is_admin', False) and booking.user_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        facade.update_booking(booking_id, {'status': 'cancelled'})
        return {'message': 'Booking cancelled successfully'}, 200
