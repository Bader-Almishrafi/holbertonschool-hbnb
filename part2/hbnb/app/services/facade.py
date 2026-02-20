from hbnb.app.persistence.repository import InMemoryRepository
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

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
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(user_data)
        return user

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

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
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity

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
            owner=owner
        )

        for a in amenities:
            place.add_amenity(a)

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

        if "owner_id" in place_data:
            new_owner = self.get_user(place_data.get("owner_id"))
            if not new_owner:
                raise ValueError("owner not found")
            place.owner = new_owner

        if "amenities" in place_data:
            amenity_ids = place_data.get("amenities")
            if not isinstance(amenity_ids, list):
                raise ValueError("amenities must be a list of amenity ids")

            place.amenities = []
            for aid in amenity_ids:
                amenity = self.get_amenity(aid)
                if not amenity:
                    raise ValueError(f"amenity not found: {aid}")
                place.add_amenity(amenity)

        scalar_updates = {}
        for k in ("title", "description", "price", "latitude", "longitude"):
            if k in place_data:
                scalar_updates[k] = place_data[k]
        if scalar_updates:
            place.update(scalar_updates)

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
            place=place,
            user=user
        )

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        allowed = {}
        for k in ("text", "rating"):
            if k in review_data:
                allowed[k] = review_data[k]

        review.update(allowed)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False

        if review.place and hasattr(review.place, "reviews"):
            if review in review.place.reviews:
                review.place.reviews.remove(review)
                review.place.save()

        self.review_repo.delete(review_id)
        return True