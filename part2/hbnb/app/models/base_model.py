# part2/hbnb/app/models/base_model.py
import uuid
from datetime import datetime


class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update updated_at whenever the object is modified."""
        self.updated_at = datetime.now()

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
