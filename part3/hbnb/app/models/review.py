from sqlalchemy.orm import validates
from hbnb.app import db
from hbnb.app.models.base_model import BaseModel


class Review(BaseModel):
    __tablename__ = 'reviews'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='uq_review_user_place'),
    )

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    def __init__(self, text, rating, user_id=None, place_id=None):
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
        self.validate()

    @validates("text")
    def validate_text(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("text is required")
        return value.strip()

    @validates("rating")
    def validate_rating(self, key, value):
        if not isinstance(value, int):
            raise ValueError("rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("rating must be between 1 and 5")
        return value

    @validates("user_id")
    def validate_user_id(self, key, value):
        if not value:
            raise ValueError("user_id is required")
        return value

    @validates("place_id")
    def validate_place_id(self, key, value):
        if not value:
            raise ValueError("place_id is required")
        return value

    def validate(self):
        if not self.text:
            raise ValueError("text is required")
        if not self.user_id:
            raise ValueError("user_id is required")
        if not self.place_id:
            raise ValueError("place_id is required")