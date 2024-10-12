"""
Contains the Comment model.
"""

from mongoengine import StringField, ReferenceField
from models.base_model import BaseModel
from models.user_model import User
from models.post_model import Post
from models.engines.db_storage import storage


class Comment(BaseModel):
    """Model representing a Comment"""
    user_id = ReferenceField(
        User, required=True, reverse_delete_rule='CASCADE'
        )
    post_id = ReferenceField(
        Post, required=False, reverse_delete_rule='CASCADE'
        )
    comment_id = ReferenceField(
        'self', required=False, reverse_delete_rule='CASCADE'
        )
    body = StringField(required=True, max_length=1000)

    def __str__(self):
        return (
            f"<Comment by User {self.user_id} "
            f"on Post {self.post_id or self.comment_id}>"
        )
