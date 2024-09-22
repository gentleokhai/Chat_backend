"""
Contains the Post model.
"""

from mongoengine import StringField, IntField, ReferenceField
from mongoengine import ListField, EmbeddedDocument, DateTimeField
from models.base_model import BaseModel
from models.user_model import User
from models.community_model import Community
from datetime import datetime, timezone


class Comment(EmbeddedDocument):
    """Embedded document for comments on a post"""
    user_id = ReferenceField(User, required=True)
    body = StringField(required=True, max_length=1000)
    likes = IntField(default=0)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))


class Post(BaseModel):
    """Model representing a Post"""
    title = StringField(required=True, max_length=200)
    body = StringField(max_length=5000)
    user_id = ReferenceField(User, required=True)
    community_id = ReferenceField(Community, required=True)
    vote_count = IntField(default=0)
    comments = ListField(Comment)

    def __str__(self):
        return f"<Post {self.title}>"
