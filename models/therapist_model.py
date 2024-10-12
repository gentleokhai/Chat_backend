#!/usr/bin/python3
"""
Contains the Therapist model.
"""

from mongoengine import StringField, ListField, ReferenceField
from models.base_model import BaseModel
from models.engines.db_storage import storage
from models.user_model import User


class Therapist(BaseModel):
    """Model representing a Therapist."""

    user_id = ReferenceField(
        User, required=True, reverse_delete_rule='CASCADE'
        )
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50)
    specialty = StringField(max_length=100)
    fees = StringField(max_length=50)
    rmdc_ref_no = StringField(max_length=100)
    qualification = StringField(max_length=200)
    availability = ListField(
        StringField(choices=['available', 'not available'])
    )
    acceptance_status = StringField(
        required=True,
        choices=['accepted', 'suspended', 'pending'],
        default='pending'
    )

    def __str__(self):
        return f"<Therapist {self.first_name} {self.last_name}>"
