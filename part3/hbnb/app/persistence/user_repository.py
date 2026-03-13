from hbnb.app.models.user import User
from hbnb.app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        if isinstance(email, str):
            email = email.strip().lower()
        return self.model.query.filter_by(email=email).first()