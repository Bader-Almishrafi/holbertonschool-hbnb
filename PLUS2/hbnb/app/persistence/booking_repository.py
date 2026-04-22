from hbnb.app.models.booking import Booking
from hbnb.app.persistence.repository import SQLAlchemyRepository


class BookingRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Booking)
