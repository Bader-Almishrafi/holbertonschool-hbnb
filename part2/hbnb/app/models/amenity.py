# part2/hbnb/app/models/amenity.py
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.validate()

    def validate(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name is required")
        if len(self.name.strip()) > 50:
            raise ValueError("name max length is 50")
