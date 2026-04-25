import re
from sqlalchemy.orm import validates
from hbnb.app import db, bcrypt
from hbnb.app.models.base_model import BaseModel

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    places = db.relationship('Place', backref='owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, email, password, is_admin=False, **kwargs):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = bool(is_admin)
        self.hash_password(password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @validates("first_name")
    def validate_first_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("first_name is required")
        value = value.strip()
        if len(value) > 255:
            raise ValueError("first_name max length is 255")
        return value

    @validates("last_name")
    def validate_last_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("last_name is required")
        value = value.strip()
        if len(value) > 255:
            raise ValueError("last_name max length is 255")
        return value

    @validates("email")
    def validate_email(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("email is required")
        value = value.strip().lower()
        if not _EMAIL_RE.match(value):
            raise ValueError("invalid email format")
        if len(value) > 255:
            raise ValueError("email max length is 255")
        return value

    @validates("is_admin")
    def validate_is_admin(self, key, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be boolean")
        return value

    def hash_password(self, raw_password):
        if not isinstance(raw_password, str) or len(raw_password.strip()) < 6:
            raise ValueError("password must be at least 6 characters")
        self.password = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def verify_password(self, raw_password):
        if not isinstance(raw_password, str) or not raw_password:
            return False
        return bcrypt.check_password_hash(self.password, raw_password)

    def validate(self):
        if not isinstance(self.password, str) or not self.password.strip():
            raise ValueError("password is required")

    def update(self, data):
        data = dict(data or {})
        if "password" in data and data["password"]:
            self.hash_password(data.pop("password"))
        super().update(data)

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.pop("password", None)
        user_dict["full_name"] = self.full_name
        return user_dict
