import uuid
from datetime import datetime
from decimal import Decimal
from hbnb.app import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def save(self):
        self.updated_at = datetime.utcnow()

    def update(self, data):
        for key, value in (data or {}).items():
            if key in ("id", "created_at", "updated_at"):
                continue
            if hasattr(self, key):
                setattr(self, key, value)

        self.save()

        if hasattr(self, "validate") and callable(getattr(self, "validate")):
            self.validate()

    def to_dict(self):
        result = {}

        for column in self.__table__.columns:
            value = getattr(self, column.name)

            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            elif isinstance(value, Decimal):
                result[column.name] = float(value)
            else:
                result[column.name] = value

        return result