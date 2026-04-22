from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def seed_demo_data():
    from hbnb.app.models.user import User
    from hbnb.app.models.amenity import Amenity
    from hbnb.app.services import facade
    if User.query.count() > 0:
        return
    admin = facade.create_user({'first_name': 'Admin', 'last_name': 'User', 'email': 'admin@example.com', 'password': '123456', 'is_admin': True})
    host = facade.create_user({'first_name': 'Bader', 'last_name': 'Host', 'email': 'host@example.com', 'password': '123456'})
    guest = facade.create_user({'first_name': 'Demo', 'last_name': 'Guest', 'email': 'guest@example.com', 'password': '123456'})
    amenities = []
    for name in ['Wi-Fi', 'Pool', 'Parking', 'Smart TV', 'Kitchen']:
        amenity = Amenity(name=name)
        db.session.add(amenity)
        amenities.append(amenity)
    db.session.commit()
    place1 = facade.create_place({'title': 'Skyline Apartment', 'description': 'Modern apartment in Riyadh with city view.', 'price': 420, 'latitude': 24.7136, 'longitude': 46.6753, 'city': 'Riyadh', 'country': 'Saudi Arabia', 'max_guests': 3, 'image_url': 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80', 'owner_id': host.id, 'amenities': [amenities[0].id, amenities[2].id, amenities[3].id]})
    place2 = facade.create_place({'title': 'Coastal Escape', 'description': 'Relaxing seaside stay with pool access.', 'price': 680, 'latitude': 21.4858, 'longitude': 39.1925, 'city': 'Jeddah', 'country': 'Saudi Arabia', 'max_guests': 5, 'image_url': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80', 'owner_id': host.id, 'amenities': [amenities[0].id, amenities[1].id, amenities[4].id]})
    facade.create_review({'text': 'Very clean and comfortable.', 'rating': 5, 'user_id': guest.id, 'place_id': place1.id})
    facade.create_booking({'user_id': guest.id, 'place_id': place1.id, 'check_in_date': '2026-05-10', 'check_out_date': '2026-05-13', 'guests': 2})


def create_app(config_class='hbnb.config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    api = Api(app, version='2.0', title='HBnB Plus API', description='HBnB Plus - Airbnb inspired booking platform API', doc='/api/v1/')

    from hbnb.app.api.v1.users import api as users_ns
    from hbnb.app.api.v1.amenities import api as amenities_ns
    from hbnb.app.api.v1.places import api as places_ns
    from hbnb.app.api.v1.reviews import api as reviews_ns
    from hbnb.app.api.v1.auth import api as auth_ns
    from hbnb.app.api.v1.bookings import api as bookings_ns
    from hbnb.app.api.v1.admin import api as admin_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(bookings_ns, path='/api/v1/bookings')
    api.add_namespace(admin_ns, path='/api/v1/admin')

    with app.app_context():
        db.create_all()
        seed_demo_data()

    return app
