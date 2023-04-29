#!/usr/bin/python
""" holds class Amenity"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import backref
import sqlalchemy
from os import getenv
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class Amenity(BaseModel, Base):
    """Amenity class handles all application amenities"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship('PlaceAmenity',
                                       backref='amenities',
                                       cascade='delete')
    else:
        name = ''
