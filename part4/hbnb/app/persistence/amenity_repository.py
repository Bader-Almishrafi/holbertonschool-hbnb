from hbnb.app.models.amenity import Amenity
from hbnb.app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)