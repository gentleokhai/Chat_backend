#!/usr/bin/python3
"""
Contains the Therapist model.
"""

from mongoengine import StringField, ListField
from models.base_model import BaseModel


class Therapist(BaseModel):
    """Model representing a Therapist."""

    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50)
    specialty = StringField(max_length=100)
    fees = StringField(max_length=50)
    availability = ListField(
        StringField(choices=['available', 'not available'])
    )
    rmdc_ref_no = StringField(max_length=100)
    qualification = StringField(max_length=200)

    def __str__(self):
        return f"<Therapist {self.first_name} {self.last_name}>"
