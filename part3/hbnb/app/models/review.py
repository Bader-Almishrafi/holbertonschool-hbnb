# part2/hbnb/app/models/review.py
from hbnb.app.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place  # Place instance
        self.user = user    # User instance

        self.validate()

        # Link review to place
        if hasattr(self.place, "add_review"):
            self.place.add_review(self)

    def validate(self):
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("text is required")

        # Accept int (and numeric that can be safely converted)
        if isinstance(self.rating, bool) or not isinstance(self.rating, (int, float)):
            raise ValueError("rating must be a number")
        if int(self.rating) != self.rating and not isinstance(self.rating, int):
            # reject non-integer floats like 4.5
            raise ValueError("rating must be an integer")
        self.rating = int(self.rating)

        if not (1 <= self.rating <= 5):
            raise ValueError("rating must be between 1 and 5")

        from hbnb.app.models.place import Place  # ✅ FIXED
        if not isinstance(self.place, Place):
            raise ValueError("place must be a Place instance")
        if not getattr(self.place, "id", None):
            raise ValueError("place must have a valid id")

        from hbnb.app.models.user import User  # ✅ FIXED
        if not isinstance(self.user, User):
            raise ValueError("user must be a User instance")
        if not getattr(self.user, "id", None):
            raise ValueError("user must have a valid id")