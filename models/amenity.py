#!/usr/bin/python3
"""Modules"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class"""
    name = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        amenity_dc = super().to_dict()
        amenity_dc['name'] = self.name
        return amenity_dc