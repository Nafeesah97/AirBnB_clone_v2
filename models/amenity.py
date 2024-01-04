#!/usr/bin/python3
""" Amenity Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv

if getenv("HBNB_TYPE_STORAGE") == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True,
                                 nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True,
                                 nullable=False)
                          )


class Amenity(BaseModel, Base):
    """ Amenity class to store Amenity information """
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        place_amenities = relationship('Place', secondary="place_amenity")
