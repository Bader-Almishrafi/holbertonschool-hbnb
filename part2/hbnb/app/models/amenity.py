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

----------------------------------------------------
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name, description=""):
        super().__init__()

        self.name = name.strip() if isinstance(name, str) else name
        self.description = description.strip() if isinstance(description, str) else description

        self.validate()

        # Many-to-many relationship
        self.places = []

    def validate(self):
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("name is required")

        if len(self.name) > 50:
            raise ValueError("name max length is 50")

        if not isinstance(self.description, str):
            raise ValueError("description must be a string")

    def update(self, data):
        if not isinstance(data, dict):
            raise ValueError("invalid update data")

        if "name" in data:
            self.name = data["name"].strip()

        if "description" in data:
            self.description = data["description"].strip()

        self.validate()

        if hasattr(self, "save"):
            self.save()

    def add_place(self, place):
        from app.models.place import Place

        if not isinstance(place, Place):
            raise ValueError("place must be a Place instance")

        if place not in self.places:
            self.places.append(place)

