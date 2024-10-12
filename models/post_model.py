"""
Contains the Post model.
"""

from mongoengine import StringField, IntField, ReferenceField
from models.base_model import BaseModel
from models.user_model import User
from models.community_model import Community
from models.engines.db_storage import storage


class Post(BaseModel):
    """Model representing a Post"""
    title = StringField(required=True, max_length=200)
    body = StringField(max_length=5000)
    user_id = ReferenceField(
        User, required=True, reverse_delete_rule='CASCADE'
        )
    community_id = ReferenceField(Community, required=True)
    vote_count = IntField(default=0)

    def __str__(self):
        return f"<Post {self.title}>"
