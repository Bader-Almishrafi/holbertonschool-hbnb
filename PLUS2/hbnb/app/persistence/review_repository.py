from hbnb.app.models.review import Review
from hbnb.app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)