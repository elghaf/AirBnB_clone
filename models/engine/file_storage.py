#!/usr/bin/python3
"""Module documentation"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.state import State
from models.review import Review
from models.city import City


class FileStorage:
    """File Storage Class"""
    __file_path = 'file.json'
    __objects = {}

    @classmethod
    def all(cls):
        """Returns the dictionary __objects"""
        return cls.__objects

    @classmethod
    def new(cls, obj):
        """Adds a new object to __objects"""

        index = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[index] = obj

    @classmethod
    def save(cls):
        """Saves __objects to a JSON file"""
        with open(cls.__file_path, 'w', encoding='utf-8') as function:
            json.dump({k: v.to_dict() for k, v in cls.__objects.items()}, function)

    @classmethod
    def reload(cls):
        """Loads objects from a JSON file"""
        class_name_mapping = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'City': City, 'State': State, 'Amenity': Amenity, 'Review': Review
        }
        try:
            with open(cls.__file_path, 'r', encoding='utf-8') as function:
                items = json.load(function).items()
                cls.__objects.update({k: class_name_mapping[v['__class__']](**v) for k, v in items})
        except FileNotFoundError:
            pass
