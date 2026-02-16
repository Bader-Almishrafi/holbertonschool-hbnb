# part2/hbnb/app/models/review.py
from app.models.base_model import BaseModel


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

        if not isinstance(self.rating, int):
            raise ValueError("rating must be an integer")
        if not (1 <= self.rating <= 5):
            raise ValueError("rating must be between 1 and 5")

        from app.models.place import Place
        if not isinstance(self.place, Place):
            raise ValueError("place must be a Place instance")
        if not getattr(self.place, "id", None):
            raise ValueError("place must have a valid id")

        from app.models.user import User
        if not isinstance(self.user, User):
            raise ValueError("user must be a User instance")
        if not getattr(self.user, "id", None):
            raise ValueError("user must have a valid id")
