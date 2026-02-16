# part2/hbnb/app/models/place.py
from app.models.base_model import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # User instance

        # Relationships
        self.reviews = []
        self.amenities = []

        self.validate()

        # Add this place to owner's places list
        if hasattr(self.owner, "add_place"):
            self.owner.add_place(self)

    def validate(self):
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("title is required")
        if len(self.title.strip()) > 100:
            raise ValueError("title max length is 100")

        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("description must be a string")

        if not isinstance(self.price, (int, float)):
            raise ValueError("price must be a number")
        if float(self.price) <= 0:
            raise ValueError("price must be a positive value")

        if not isinstance(self.latitude, (int, float)):
            raise ValueError("latitude must be a number")
        if not (-90.0 <= float(self.latitude) <= 90.0):
            raise ValueError("latitude must be between -90.0 and 90.0")

        if not isinstance(self.longitude, (int, float)):
            raise ValueError("longitude must be a number")
        if not (-180.0 <= float(self.longitude) <= 180.0):
            raise ValueError("longitude must be between -180.0 and 180.0")

        # owner must exist (in this stage: validate it's a User instance with id)
        from app.models.user import User
        if not isinstance(self.owner, User):
            raise ValueError("owner must be a User instance")
        if not getattr(self.owner, "id", None):
            raise ValueError("owner must have a valid id")

    def add_review(self, review):
        from app.models.review import Review

        if not isinstance(review, Review):
            raise ValueError("review must be a Review instance")
        if review.place != self:
            raise ValueError("review.place must be this place")
        if review not in self.reviews:
            self.reviews.append(review)
            self.save()

    def add_amenity(self, amenity):
        from app.models.amenity import Amenity

        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    def remove_amenity(self, amenity):
        from app.models.amenity import Amenity

        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")
        if amenity in self.amenities:
            self.amenities.remove(amenity)
            self.save()
