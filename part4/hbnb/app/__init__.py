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
    from datetime import date, timedelta
    from hbnb.app.models.user import User
    from hbnb.app.models.amenity import Amenity
    from hbnb.app.services import facade

    if User.query.count() > 0:
        return

    facade.create_user({'first_name': 'Admin', 'last_name': 'User', 'email': 'admin@example.com', 'password': '123456', 'is_admin': True})

    host_specs = [
        ('Bader', 'Host', 'host@example.com'),
        ('Nora', 'Host', 'nora.host@example.com'),
        ('Faisal', 'Host', 'faisal.host@example.com'),
        ('Lama', 'Host', 'lama.host@example.com'),
    ]
    guest_specs = [
        ('Demo', 'Guest', 'guest@example.com'),
        ('Sara', 'Ali', 'sara@example.com'),
        ('Omar', 'Khalid', 'omar@example.com'),
        ('Reem', 'Saad', 'reem@example.com'),
        ('Yousef', 'Nasser', 'yousef@example.com'),
        ('Huda', 'Fahad', 'huda@example.com'),
        ('Mazen', 'Ammar', 'mazen@example.com'),
        ('Raghad', 'Adel', 'raghad@example.com'),
    ]

    hosts = [facade.create_user({'first_name': f, 'last_name': l, 'email': e, 'password': '123456'}) for f, l, e in host_specs]
    guests = [facade.create_user({'first_name': f, 'last_name': l, 'email': e, 'password': '123456'}) for f, l, e in guest_specs]

    amenity_names = ['Wi-Fi', 'Pool', 'Parking', 'Smart TV', 'Kitchen', 'Workspace', 'Gym', 'Balcony', 'Breakfast', 'Washer']
    amenities = []
    for name in amenity_names:
        amenity = Amenity(name=name)
        db.session.add(amenity)
        amenities.append(amenity)
    db.session.commit()

    place_specs = [
        ('Skyline Apartment', 'Modern apartment in Riyadh with skyline views.', 420, 24.7136, 46.6753, 'Riyadh', 3, 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80'),
        ('Coastal Escape', 'Relaxing seaside stay near Jeddah corniche.', 680, 21.4858, 39.1925, 'Jeddah', 5, 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80'),
        ('Desert Retreat', 'Warm desert-inspired villa with private lounge.', 590, 18.2164, 42.5053, 'Abha', 4, 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80'),
        ('Business Loft', 'Perfect downtown loft for short work trips.', 350, 24.6877, 46.7219, 'Riyadh', 2, 'https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80'),
        ('Family Villa', 'Large family villa with garden and pool.', 900, 26.4207, 50.0888, 'Dammam', 7, 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=1200&q=80'),
        ('Studio 88', 'Compact stylish studio for solo travelers.', 260, 21.3891, 39.8579, 'Makkah', 2, 'https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1200&q=80'),
        ('Palm Residence', 'Quiet residence with balcony and city access.', 480, 24.7743, 46.7386, 'Riyadh', 4, 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80'),
        ('Sea Breeze Flat', 'Bright flat with sea breeze and sunset views.', 530, 21.5433, 39.1728, 'Jeddah', 3, 'https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80'),
        ('Mountain Cabin', 'Peaceful cabin-style stay with cool weather.', 610, 21.2703, 40.4158, 'Taif', 4, 'https://images.unsplash.com/photo-1449844908441-8829872d2607?auto=format&fit=crop&w=1200&q=80'),
        ('Art House', 'Creative interior with premium amenities.', 455, 26.3927, 49.9777, 'Khobar', 3, 'https://images.unsplash.com/photo-1460317442991-0ec209397118?auto=format&fit=crop&w=1200&q=80'),
        ('Garden Suite', 'Green and calm suite for couples.', 390, 24.5247, 39.5692, 'Madinah', 2, 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80'),
        ('Luxury Penthouse', 'Top-floor premium penthouse for special stays.', 1200, 24.7131, 46.6749, 'Riyadh', 6, 'https://images.unsplash.com/photo-1502672023488-70e25813eb80?auto=format&fit=crop&w=1200&q=80')
    ]

    places = []
    for idx, spec in enumerate(place_specs):
        title, description, price, lat, lng, city, max_guests, image_url = spec
        owner = hosts[idx % len(hosts)]
        selected_amenities = [amenities[(idx + offset) % len(amenities)].id for offset in range(3)]
        places.append(facade.create_place({
            'title': title,
            'description': description,
            'price': price,
            'latitude': lat,
            'longitude': lng,
            'city': city,
            'country': 'Saudi Arabia',
            'max_guests': max_guests,
            'image_url': image_url,
            'owner_id': owner.id,
            'amenities': selected_amenities,
        }))

    review_texts = [
        'Excellent stay and very clean.', 'Smooth check-in and great host.', 'Location was perfect for our trip.',
        'Would definitely book again.', 'Comfortable stay with nice amenities.', 'Great value for money.'
    ]
    for idx, place in enumerate(places):
        selected_guests = guests[: (idx % 3) + 2]
        for guest in selected_guests:
            facade.create_review({
                'text': review_texts[(idx + len(guest.first_name)) % len(review_texts)],
                'rating': 4 + ((idx + len(guest.last_name)) % 2),
                'user_id': guest.id,
                'place_id': place.id,
            })

    start_base = date(2026, 5, 1)
    for idx, place in enumerate(places):
        for slot in range(4):
            guest = guests[(idx + slot) % len(guests)]
            check_in = start_base + timedelta(days=idx * 3 + slot * 9)
            check_out = check_in + timedelta(days=2 + (slot % 3))
            status = 'cancelled' if (idx + slot) % 5 == 0 else ('pending' if (idx + slot) % 4 == 0 else 'confirmed')
            facade.create_booking({
                'user_id': guest.id,
                'place_id': place.id,
                'check_in_date': check_in.isoformat(),
                'check_out_date': check_out.isoformat(),
                'guests': min(place.max_guests, 1 + ((idx + slot) % place.max_guests)),
                'status': status,
            })



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
