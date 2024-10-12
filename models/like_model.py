#!/usr/bin/python3
"""
Contains the Like model.
"""

from mongoengine import ReferenceField, IntField
from models.base_model import BaseModel
from models.therapist_model import Therapist
from models.user_model import User
from models.post_model import Post
from models.comment_model import Comment
from models.engines.db_storage import storage


class Like(BaseModel):
    """Model representing a Like on a post or comment or a Therapist"""
    user_id = ReferenceField(User, reverse_delete_rule='CASCADE')
    post_id = ReferenceField(Post, reverse_delete_rule='CASCADE')
    comment_id = ReferenceField(Comment, reverse_delete_rule='CASCADE')
    therapist_id = ReferenceField(Therapist, reverse_delete_rule='CASCADE')
    value = IntField(choices=[1, -1], required=True)

    def __str__(self):
        return (f"<Like {self.user_id} -> "
                f"{self.post_id or self.comment_id or self.therapist_id}>")
