#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        _cities_relationship = relationship('City',
                                            backref='state',
                                            cascade='delete')
        
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def _get_cities(self):
            from models import storage
            '''returns the list of City instances with state_id
                    equals the current State.id
                    FileStorage relationship between State and City
            '''
            _cities = []
            cities = storage.all(City)
            for city in cities.values():
                    if city.state_id == self.id:
                        _cities.append(city)
            return _cities
