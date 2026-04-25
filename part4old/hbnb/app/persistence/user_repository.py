from hbnb.app.models.user import User
from hbnb.app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        return self.get_by_attribute("email", email)