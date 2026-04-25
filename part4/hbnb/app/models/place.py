from sqlalchemy.orm import validates
from hbnb.app import db
from hbnb.app.models.base_model import BaseModel

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(120), nullable=False, default='Riyadh')
    country = db.Column(db.String(120), nullable=False, default='Saudi Arabia')
    max_guests = db.Column(db.Integer, nullable=False, default=2)
    image_url = db.Column(db.String(500), nullable=True)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='place', lazy=True, cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery', backref=db.backref('places', lazy=True))

    def __init__(self, title, description=None, price=0, latitude=0.0, longitude=0.0, city='Riyadh', country='Saudi Arabia', max_guests=2, image_url=None, owner_id=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.country = country
        self.max_guests = max_guests
        self.image_url = image_url
        self.owner_id = owner_id
        self.validate()

    @validates("title")
    def validate_title(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("title is required")
        value = value.strip()
        if len(value) > 255:
            raise ValueError("title max length is 255")
        return value

    @validates("description")
    def validate_description(self, key, value):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("description must be a string")
        return value.strip()

    @validates("price")
    def validate_price(self, key, value):
        if not isinstance(value, (int, float)):
            raise ValueError("price must be a number")
        if value < 0:
            raise ValueError("price must be positive")
        return value

    @validates("latitude")
    def validate_latitude(self, key, value):
        if not isinstance(value, (int, float)):
            raise ValueError("latitude must be a number")
        if value < -90 or value > 90:
            raise ValueError("latitude must be between -90 and 90")
        return float(value)

    @validates("longitude")
    def validate_longitude(self, key, value):
        if not isinstance(value, (int, float)):
            raise ValueError("longitude must be a number")
        if value < -180 or value > 180:
            raise ValueError("longitude must be between -180 and 180")
        return float(value)

    @validates("owner_id")
    def validate_owner_id(self, key, value):
        if not value:
            raise ValueError("owner_id is required")
        return value

    @validates('city', 'country')
    def validate_text_fields(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'{key} is required')
        return value.strip()

    @validates('max_guests')
    def validate_max_guests(self, key, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError('max_guests must be a positive integer')
        return value

    def validate(self):
        if not self.title:
            raise ValueError("title is required")
        if not self.owner_id:
            raise ValueError("owner_id is required")

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    @property
    def average_rating(self):
        if not self.reviews:
            return None
        return round(sum(review.rating for review in self.reviews) / len(self.reviews), 1)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": float(self.price) if self.price is not None else None,
            "latitude": float(self.latitude) if self.latitude is not None else None,
            "longitude": float(self.longitude) if self.longitude is not None else None,
            "city": self.city,
            "country": self.country,
            "max_guests": self.max_guests,
            "image_url": self.image_url,
            "owner_id": self.owner_id,
            "amenities": [amenity.id for amenity in self.amenities],
            "average_rating": self.average_rating,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
