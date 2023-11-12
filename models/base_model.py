#!/usr/bin/python3
"""Module documentation"""
from datetime import datetime
import uuid
import models


class BaseModel:
    """BaseModel is the parent class"""

    def __init__(self, *args, **kwargs):
        """Initializer method."""
        if kwargs:
            self.__load_from_dict(kwargs)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            models.storage.new(self)

    def __load_from_dict(self, dictionary):
        """Load data from dictionary."""
        self.__dict__.update(dictionary)
        self.__dict__.pop('__class__', None)

        for attr in ('created_at', 'updated_at'):
            if attr in self.__dict__:
                self.__dict__[attr] = datetime.fromisoformat(
                    self.__dict__[attr])

    def __str__(self):
        """String representation of the object."""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__)

    def save(self):
        """Update the public instance attribute updated_at."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return a dictionary containing all keys/values of the instance."""
        obj_dict = {**self.__dict__}
        for attr in ('created_at', 'updated_at'):
            if attr in obj_dict:
                obj_dict[attr] = obj_dict[attr].isoformat()
        obj_dict['__class__'] = self.__class__.__name__
        return obj_dict
