from datetime import date
from sqlalchemy.orm import validates
from hbnb.app import db
from hbnb.app.models.base_model import BaseModel


class Booking(BaseModel):
    __tablename__ = 'bookings'

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False, index=True)
    check_in_date = db.Column(db.Date, nullable=False, index=True)
    check_out_date = db.Column(db.Date, nullable=False, index=True)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='confirmed')
    guests = db.Column(db.Integer, nullable=False, default=1)

    VALID_STATUSES = {'pending', 'confirmed', 'cancelled'}

    def __init__(self, user_id, place_id, check_in_date, check_out_date, total_price, status='confirmed', guests=1, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.place_id = place_id
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.total_price = total_price
        self.status = status
        self.guests = guests
        self.validate()

    @validates('status')
    def validate_status(self, key, value):
        if value not in self.VALID_STATUSES:
            raise ValueError('status must be pending, confirmed, or cancelled')
        return value

    @validates('guests')
    def validate_guests(self, key, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError('guests must be a positive integer')
        return value

    def validate(self):
        if not self.user_id:
            raise ValueError('user_id is required')
        if not self.place_id:
            raise ValueError('place_id is required')
        if not isinstance(self.check_in_date, date) or not isinstance(self.check_out_date, date):
            raise ValueError('check-in and check-out dates are required')
        if self.check_out_date <= self.check_in_date:
            raise ValueError('check_out_date must be after check_in_date')
        if float(self.total_price) < 0:
            raise ValueError('total_price must be positive')
