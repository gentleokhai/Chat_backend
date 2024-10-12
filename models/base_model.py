#!/usr/bin/python3
"""
Contains the BaseModel class for MongoDB models.
"""

from datetime import datetime, timezone
import uuid
from mongoengine import Document, StringField, DateTimeField, ReferenceField


class BaseModel(Document):
    """The BaseModel class from which other models will be derived"""
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    created_by = ReferenceField('User', required=False)
    updated_by = ReferenceField('User', required=False)

    meta = {'abstract': True}

    def save(self, *args, **kwargs):
        """Override save to update `updated_at` and `updated_by` fields"""
        # Update 'updated_by' field when saving
        if 'updated_by' in kwargs:
            self.updated_by = kwargs.pop('updated_by')
        self.updated_at = datetime.now(timezone.utc)

        # Set 'created_by' only once when creating the object
        if not self.created_at and 'created_by' in kwargs:
            self.created_by = kwargs.pop('created_by')

        return super().save(*args, **kwargs)

    def to_dict(self):
        """Return a dictionary representation of the instance"""
        return self.to_mongo().to_dict()

    def delete(self, *args, **kwargs):
        """Delete the current instance"""
        return super().delete(*args, **kwargs)
