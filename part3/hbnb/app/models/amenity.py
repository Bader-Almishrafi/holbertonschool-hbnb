from sqlalchemy.orm import validates
from hbnb.app import db
from hbnb.app.models.base_model import BaseModel


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name
        self.validate()

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("name is required")
        value = value.strip()
        if len(value) > 100:
            raise ValueError("name max length is 100")
        return value

    def validate(self):
        if not self.name:
            raise ValueError("name is required")