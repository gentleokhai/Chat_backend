"""
Contains the Comment model.
"""

from mongoengine import StringField, IntField, ReferenceField
from models.base_model import BaseModel
from models.user_model import User
from models.post_model import Post


class Comment(BaseModel):
    """Model representing a Comment"""
    user_id = ReferenceField(User, required=True)
    post_id = ReferenceField(Post, required=False)
    comment_id = ReferenceField('self', required=False)
    body = StringField(required=True, max_length=1000)

    def __str__(self):
        return (
            f"<Comment by User {self.user_id} "
            f"on Post {self.post_id or self.comment_id}>"
        )
