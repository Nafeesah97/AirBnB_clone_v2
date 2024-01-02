#!/usr/bin/python3
"""This is the amenity class"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String

class Amenity(BaseModel, Base):
    """This is the class for Amenity
    Attributes:
        name: input name
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False
    place_amenities = None  # Placeholder for circular import resolution

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        @property
        def place_amenities(self):
            '''
            Returns the relationship with Place and
            resolves circular import issue
            '''
            from models.place import place_amenity
            return relationship("Place", secondary=place_amenity)
