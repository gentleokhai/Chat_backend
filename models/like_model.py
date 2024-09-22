#!/usr/bin/python3
"""
Contains the Like model.
"""

from mongoengine import ReferenceField, IntField, StringField
from models.base_model import BaseModel
from models.user_model import User
from models.post_model import Post


class Like(BaseModel):
    """Model representing a Like on a post or comment"""
    user_id = ReferenceField(User, required=True)
    post_id = ReferenceField(Post)
    comment_id = StringField()  # Only one of post_id or comment_id will be set
    value = IntField(choices=[1, -1], required=True)

    def __str__(self):
        return f"<Like {self.user_id} -> {self.post_id or self.comment_id}>"