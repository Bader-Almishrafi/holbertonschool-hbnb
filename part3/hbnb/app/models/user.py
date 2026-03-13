import re
from hbnb.app import db
from hbnb.app.models.base_model import BaseModel

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(BaseModel, db.Model):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column('password', db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    _used_emails = set()

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self._password = None
        self.hash_password(password)
        self.is_admin = bool(is_admin)

        self.validate()

        self.places = []

    @classmethod
    def _reset_used_emails(cls):
        cls._used_emails = set()

    def _register_email(self, email):
        normalized = email.strip().lower()
        if normalized in User._used_emails:
            raise ValueError("email must be unique")
        User._used_emails.add(normalized)

    def _unregister_email(self, email):
        normalized = email.strip().lower()
        User._used_emails.discard(normalized)

    @property
    def password(self):
        return self._password

    def hash_password(self, raw_password):
        """Hashes the password before storing it."""
        if not isinstance(raw_password, str) or not raw_password.strip():
            raise ValueError("password is required")

        from hbnb.app import bcrypt
        hashed = bcrypt.generate_password_hash(raw_password)
        self._password = hashed.decode("utf-8")

    @password.setter
    def password(self, raw_password):
        self.hash_password(raw_password)

    def verify_password(self, raw_password):
        """Verifies if the provided password matches the hashed password."""
        if not isinstance(raw_password, str) or not raw_password:
            return False

        from hbnb.app import bcrypt
        return bcrypt.check_password_hash(self._password, raw_password)

    def validate(self):
        if not isinstance(self.first_name, str) or not self.first_name.strip():
            raise ValueError("first_name is required")
        if len(self.first_name.strip()) > 50:
            raise ValueError("first_name max length is 50")

        if not isinstance(self.last_name, str) or not self.last_name.strip():
            raise ValueError("last_name is required")
        if len(self.last_name.strip()) > 50:
            raise ValueError("last_name max length is 50")

        if not isinstance(self.email, str) or not self.email.strip():
            raise ValueError("email is required")
        if not _EMAIL_RE.match(self.email.strip()):
            raise ValueError("invalid email format")

        if not isinstance(self._password, str) or not self._password.strip():
            raise ValueError("password is required")

        if not isinstance(self.is_admin, bool):
            raise ValueError("is_admin must be boolean")

    def update(self, data):
        data = dict(data or {})
        old_email = self.email

        if "password" in data:
            self.hash_password(data.pop("password"))

        if "email" in data:
            new_email = data["email"]
            if not isinstance(new_email, str) or not new_email.strip():
                raise ValueError("email is required")
            if not _EMAIL_RE.match(new_email.strip()):
                raise ValueError("invalid email format")

        super().update(data)

        if "email" in data and self.email.strip().lower() != old_email.strip().lower():
            pass

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.pop("_password", None)
        user_dict.pop("password", None)
        return user_dict

    def add_place(self, place):
        from hbnb.app.models.place import Place
        if not isinstance(place, Place):
            raise ValueError("place must be a Place instance")
        if place.owner != self:
            raise ValueError("place.owner must be this user")
        if place not in self.places:
            self.places.append(place)
            self.save()