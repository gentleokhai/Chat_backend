#!/usr/bin/python3
"""
Contains the BaseModel class for MongoDB models.
"""

from datetime import datetime, timezone
import uuid
from mongoengine import Document, StringField, DateTimeField


class BaseModel(Document):
    """The BaseModel class from which other models will be derived"""
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {'abstract': True}

    def save(self, *args, **kwargs):
        """Override save to update `updated_at` field"""
        self.updated_at = datetime.now(timezone.utc)
        return super().save(*args, **kwargs)

    def to_dict(self):
        """Return a dictionary representation of the instance"""
        return self.to_mongo().to_dict()

    def delete(self, *args, **kwargs):
        """Delete the current instance"""
        return super().delete(*args, **kwargs)
