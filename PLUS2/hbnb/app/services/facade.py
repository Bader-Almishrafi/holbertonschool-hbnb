from datetime import datetime
from sqlalchemy import func, or_
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review
from hbnb.app.models.booking import Booking
from hbnb.app.persistence.user_repository import UserRepository
from hbnb.app.persistence.amenity_repository import AmenityRepository
from hbnb.app.persistence.place_repository import PlaceRepository
from hbnb.app.persistence.review_repository import ReviewRepository
from hbnb.app.persistence.booking_repository import BookingRepository
from hbnb.app import db


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = AmenityRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.booking_repo = BookingRepository()

    def create_user(self, user_data):
        existing_user = self.user_repo.get_by_email(user_data.get("email"))
        if existing_user:
            raise ValueError("Email already registered")
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_email(email)

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)

    def create_place(self, place_data):
        owner_id = place_data.get("owner_id")
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("owner not found")
        amenity_ids = place_data.get("amenities", [])
        if not isinstance(amenity_ids, list):
            raise ValueError("amenities must be a list of amenity ids")
        amenities = []
        for aid in amenity_ids:
            amenity = self.get_amenity(aid)
            if not amenity:
                raise ValueError(f"amenity not found: {aid}")
            amenities.append(amenity)
        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description", ""),
            price=place_data.get("price"),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            city=place_data.get("city", "Riyadh"),
            country=place_data.get("country", "Saudi Arabia"),
            max_guests=place_data.get("max_guests", 2),
            image_url=place_data.get("image_url"),
            owner_id=owner_id
        )
        for amenity in amenities:
            place.add_amenity(amenity)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self, city=None, max_price=None, q=None):
        query = Place.query
        if city:
            query = query.filter(Place.city.ilike(f"%{city}%"))
        if max_price is not None:
            query = query.filter(Place.price <= max_price)
        if q:
            query = query.filter(or_(Place.title.ilike(f"%{q}%"), Place.description.ilike(f"%{q}%"), Place.city.ilike(f"%{q}%")))
        return query.order_by(Place.created_at.desc()).all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None
        data = dict(place_data or {})
        data.pop("owner_id", None)
        if "amenities" in data:
            amenity_ids = data.pop("amenities")
            if not isinstance(amenity_ids, list):
                raise ValueError("amenities must be a list of amenity ids")
            amenities = []
            for aid in amenity_ids:
                amenity = self.get_amenity(aid)
                if not amenity:
                    raise ValueError(f"amenity not found: {aid}")
                amenities.append(amenity)
            place.amenities = amenities
        if data:
            place.update(data)
        else:
            db.session.commit()
        return place

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    def create_review(self, review_data):
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")
        user = self.get_user(user_id)
        if not user:
            raise ValueError("user not found")
        place = self.get_place(place_id)
        if not place:
            raise ValueError("place not found")
        review = Review(text=review_data.get("text"), rating=review_data.get("rating"), user_id=user_id, place_id=place_id)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        return place.reviews if place else []

    def update_review(self, review_id, review_data):
        data = dict(review_data or {})
        data.pop("user_id", None)
        data.pop("place_id", None)
        return self.review_repo.update(review_id, data)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)

    def _parse_date(self, value):
        return value if hasattr(value, 'isoformat') and not isinstance(value, str) else datetime.strptime(value, '%Y-%m-%d').date()

    def booking_conflicts(self, place_id, check_in_date, check_out_date, exclude_booking_id=None):
        query = Booking.query.filter(Booking.place_id == place_id, Booking.status != 'cancelled', Booking.check_in_date < check_out_date, Booking.check_out_date > check_in_date)
        if exclude_booking_id:
            query = query.filter(Booking.id != exclude_booking_id)
        return query.first() is not None

    def create_booking(self, booking_data):
        user = self.get_user(booking_data.get('user_id'))
        place = self.get_place(booking_data.get('place_id'))
        if not user:
            raise ValueError('user not found')
        if not place:
            raise ValueError('place not found')
        check_in_date = self._parse_date(booking_data.get('check_in_date'))
        check_out_date = self._parse_date(booking_data.get('check_out_date'))
        guests = int(booking_data.get('guests', 1))
        if guests > place.max_guests:
            raise ValueError('guests exceed place capacity')
        if self.booking_conflicts(place.id, check_in_date, check_out_date):
            raise ValueError('selected dates are not available')
        total_price = (check_out_date - check_in_date).days * float(place.price)
        booking = Booking(user_id=user.id, place_id=place.id, check_in_date=check_in_date, check_out_date=check_out_date, total_price=total_price, status=booking_data.get('status', 'confirmed'), guests=guests)
        self.booking_repo.add(booking)
        return booking

    def get_booking(self, booking_id):
        return self.booking_repo.get(booking_id)

    def get_all_bookings(self, user_id=None, status=None):
        query = Booking.query
        if user_id:
            query = query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Booking.created_at.desc()).all()

    def update_booking(self, booking_id, booking_data):
        booking = self.get_booking(booking_id)
        if not booking:
            return None
        data = dict(booking_data or {})
        if 'status' in data and data['status'] not in Booking.VALID_STATUSES:
            raise ValueError('invalid booking status')
        if 'guests' in data:
            data['guests'] = int(data['guests'])
            if data['guests'] > booking.place.max_guests:
                raise ValueError('guests exceed place capacity')
        if 'check_in_date' in data or 'check_out_date' in data:
            check_in = self._parse_date(data.get('check_in_date', booking.check_in_date.isoformat()))
            check_out = self._parse_date(data.get('check_out_date', booking.check_out_date.isoformat()))
            if self.booking_conflicts(booking.place_id, check_in, check_out, exclude_booking_id=booking.id):
                raise ValueError('selected dates are not available')
            data['check_in_date'] = check_in
            data['check_out_date'] = check_out
            data['total_price'] = (check_out - check_in).days * float(booking.place.price)
        booking.update(data)
        return booking

    def delete_booking(self, booking_id):
        return self.booking_repo.delete(booking_id)

    def get_admin_stats(self):
        return {
            'users': User.query.count(),
            'places': Place.query.count(),
            'reviews': Review.query.count(),
            'bookings': Booking.query.count(),
            'confirmed_bookings': Booking.query.filter_by(status='confirmed').count(),
            'cancelled_bookings': Booking.query.filter_by(status='cancelled').count(),
            'revenue': float(db.session.query(func.coalesce(func.sum(Booking.total_price), 0)).filter(Booking.status == 'confirmed').scalar() or 0)
        }


facade = HBnBFacade()
