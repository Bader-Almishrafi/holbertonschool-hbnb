import re
from sqlalchemy.orm import validates
from hbnb.app import db, bcrypt
from hbnb.app.models.base_model import BaseModel

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = bool(is_admin)
        self.hash_password(password)
        self.validate()

    @validates("first_name")
    def validate_first_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("first_name is required")
        value = value.strip()
        if len(value) > 50:
            raise ValueError("first_name max length is 50")
        return value

    @validates("last_name")
    def validate_last_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("last_name is required")
        value = value.strip()
        if len(value) > 50:
            raise ValueError("last_name max length is 50")
        return value

    @validates("email")
    def validate_email(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("email is required")
        value = value.strip().lower()
        if not _EMAIL_RE.match(value):
            raise ValueError("invalid email format")
        return value

    @validates("is_admin")
    def validate_is_admin(self, key, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be boolean")
        return value

    def hash_password(self, raw_password):
        """Hashes the password before storing it."""
        if not isinstance(raw_password, str) or not raw_password.strip():
            raise ValueError("password is required")

        self.password = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def verify_password(self, raw_password):
        """Verifies if the provided password matches the hashed password."""
        if not isinstance(raw_password, str) or not raw_password:
            return False
        return bcrypt.check_password_hash(self.password, raw_password)

    def validate(self):
        if not isinstance(self.password, str) or not self.password.strip():
            raise ValueError("password is required")

    def update(self, data):
        data = dict(data or {})

        if "password" in data:
            self.hash_password(data.pop("password"))

        super().update(data)

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.pop("password", None)
        return user_dict