#!/usr/bin/python3
"""
BaseModel Class of Models Module
"""

import os
import json
import models
from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
import sqlalchemy
from os import getenv

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')

if STORAGE_TYPE == 'db':
    Base = declarative_base()
else:
    class Base:
        pass



class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
            instantiation of new BaseModel Class
        """
        if kwargs:
            self.__set_attributes(kwargs)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()

    def __set_attributes(self, attr_dict):
        """
            private: converts attr_dict values to python class attributes
        """
        if 'id' not in attr_dict:
            attr_dict['id'] = str(uuid4())
        if 'created_at' not in attr_dict:
            attr_dict['created_at'] = datetime.utcnow()
        elif not isinstance(attr_dict['created_at'], datetime):
            attr_dict['created_at'] = datetime.strptime(
                attr_dict['created_at'], "%Y-%m-%d %H:%M:%S.%f"
            )
        if 'updated_at' not in attr_dict:
            attr_dict['updated_at'] = datetime.utcnow()
        elif not isinstance(attr_dict['updated_at'], datetime):
            attr_dict['updated_at'] = datetime.strptime(
                attr_dict['updated_at'], "%Y-%m-%d %H:%M:%S.%f"
            )
        if STORAGE_TYPE != 'db':
            attr_dict.pop('__class__', None)
        for attr, val in attr_dict.items():
            setattr(self, attr, val)

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)
    def __is_serializable(self, obj_v):
        """
            private: checks if object is serializable
        """
        try:
            obj_to_str = json.dumps(obj_v)
            return obj_to_str is not None and isinstance(obj_to_str, str)
        except:
            return False

    def update(self, ignore, *args, **kwargs):
        """updates the instance using a dictionary of kwargs"""
        for k, v in kwargs.items():
            if k in ignore:
                continue
            setattr(self, k, v)
        self.save()

    def save(self):
        """
            updates attribute updated_at to current time
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_json(self, saving_file_storage=False):
        """
            returns json representation of self
        """
        obj_class = self.__class__.__name__
        bm_dict = {
            k: v if self.__is_serializable(v) else str(v)
            for k, v in self.__dict__.items()
        }
        bm_dict.pop('_sa_instance_state', None)
        bm_dict.update({
            '__class__': obj_class
            })
        if not saving_file_storage and obj_class == 'User':
            bm_dict.pop('password', None)
        return(bm_dict)

    def to_dict(self, save_pass=False):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        if "password" in new_dict and not save_pass:
            new_dict.pop("password")
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
