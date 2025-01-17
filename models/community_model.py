#!/usr/bin/python3
"""
Contains the Community model.
"""

from mongoengine import StringField, ListField, ReferenceField
from models.base_model import BaseModel
from models.user_model import User
from models.engines.db_storage import storage


class Community(BaseModel):
    """Model representing a Community (like a subreddit)"""
    name = StringField(required=True, unique=True, max_length=100)
    description = StringField(max_length=500)
    moderators = ListField(
        ReferenceField(User, reverse_delete_rule='CASCADE')
        )

    def __str__(self):
        return f"<Community {self.name}>"
