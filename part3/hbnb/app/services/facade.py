from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review
from hbnb.app.persistence.repository import SQLAlchemyRepository
from hbnb.app.persistence.user_repository import UserRepository
from hbnb.app import db


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)

    # ---------- Users ----------
    def create_user(self, user_data):
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
        return self.user_repo.get_user_by_email(email)

    # ---------- Amenities ----------
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

    # ---------- Places ----------
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
            owner_id=owner_id
        )

        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None

        data = dict(place_data or {})

        if "owner_id" in data:
            data.pop("owner_id")

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

        db.session.commit()
        return place

    # ---------- Reviews ----------
    def create_review(self, review_data):
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        user = self.get_user(user_id)
        if not user:
            raise ValueError("user not found")

        place = self.get_place(place_id)
        if not place:
            raise ValueError("place not found")

        review = Review(
            text=review_data.get("text"),
            rating=review_data.get("rating"),
            user_id=user_id,
            place_id=place_id
        )

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return Review.query.filter_by(place_id=place_id).all()

    def update_review(self, review_id, review_data):
        data = dict(review_data or {})
        data.pop("user_id", None)
        data.pop("place_id", None)
        return self.review_repo.update(review_id, data)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)