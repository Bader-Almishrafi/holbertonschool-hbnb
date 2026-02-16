from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
place = Place(
    title="Cozy Apartment",
    description="A nice place to stay",
    price=100,
    latitude=37.7749,
    longitude=-122.4194,
    owner=owner
)

review = Review(text="Great stay!", rating=5, place=place, user=owner)
amenity = Amenity(name="Wi-Fi")
place.add_amenity(amenity)

print("User places:", len(owner.places))
print("Place reviews:", len(place.reviews))
print("Place amenities:", len(place.amenities))
print("OK")
