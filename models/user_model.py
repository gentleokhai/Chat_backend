#!/usr/bin/python3
"""
Contains the User model.
"""

from mongoengine import StringField, ListField, IntField, EmbeddedDocumentField
from models.base_model import BaseModel


class User(BaseModel):
    """Model representing a User"""
    username = StringField(required=True, unique=True, max_length=50)
    role = ListField(StringField(choices=['admin', 'therapist', 'user']))
    email = StringField(required=True, unique=True, max_length=100)
    password_hash = StringField(required=True)
    karma = IntField(default=0)

    def __str__(self):
        return f"<User {self.username}>"
