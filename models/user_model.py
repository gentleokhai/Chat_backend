#!/usr/bin/python3
"""
Contains the User model.
"""

from mongoengine import StringField, ListField, IntField, BooleanField
from models.base_model import BaseModel


class User(BaseModel):
    """Model representing a User"""
    username = StringField(required=True, unique=True, max_length=50)
    role = ListField(
        StringField(
            choices=['admin', 'user']
            ), default=["user"]
        )
    email = StringField(required=True, unique=True, max_length=100)
    password_hash = StringField(required=True)
    karma = IntField(default=0)
    is_superuser = BooleanField(default=False)
    status = StringField(
        choices=['blocked', 'active', 'pending'],
        default='pending',
        required=True
    )

    def __str__(self):
        return f"<User {self.username}>"
