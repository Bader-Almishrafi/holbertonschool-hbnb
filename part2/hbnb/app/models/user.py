# part2/hbnb/app/models/user.py
import re
from hbnb.app.models.base_model import BaseModel

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(BaseModel):
    _used_emails = set()  # in-memory uniqueness tracker (note: persists while app is running)

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = bool(is_admin)

        self.validate()
        self._register_email(self.email)

        # Relationship (one-to-many): user -> places
        self.places = []

    @classmethod
    def _reset_used_emails(cls):
        """Helper for tests (optional)."""
        cls._used_emails = set()

    def _register_email(self, email):
        normalized = email.strip().lower()
        if normalized in User._used_emails:
            raise ValueError("email must be unique")
        User._used_emails.add(normalized)

    def _unregister_email(self, email):
        normalized = email.strip().lower()
        User._used_emails.discard(normalized)

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

        if not isinstance(self.is_admin, bool):
            raise ValueError("is_admin must be boolean")

    def update(self, data):
        # handle email uniqueness if email is being changed
        old_email = self.email
        super().update(data)
        if "email" in (data or {}) and self.email != old_email:
            self._unregister_email(old_email)
            self._register_email(self.email)

    def add_place(self, place):
        # Lazy import to avoid circular imports
        from hbnb.app.models.place import Place  # ✅ FIXED

        if not isinstance(place, Place):
            raise ValueError("place must be a Place instance")
        if place.owner != self:
            raise ValueError("place.owner must be this user")
        if place not in self.places:
            self.places.append(place)
            self.save()