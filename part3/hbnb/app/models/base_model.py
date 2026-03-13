# part3/hbnb/app/models/base_model.py

import uuid
from datetime import datetime
from hbnb.app import db


class BaseModel:
    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def save(self):
        """Update updated_at whenever the object is modified."""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """Update object attributes from dict and refresh updated_at."""
        for key, value in (data or {}).items():
            if key in ("id", "created_at", "updated_at"):
                continue

            if hasattr(self, key):
                setattr(self, key, value)

        self.save()

        # validate after updates if validate() exists
        if hasattr(self, "validate") and callable(getattr(self, "validate")):
            self.validate()

    def to_dict(self):
        """Convert SQLAlchemy object to dictionary."""
        result = {}

        for column in self.__table__.columns:
            value = getattr(self, column.name)

            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value

        return result