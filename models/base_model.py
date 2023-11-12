#!/usr/bin/python3

import uuid
from datetime import datetime
from models import storage

def __init__(self, *args, **kwargs):
    """Initializes all attributes associated"""
    if not kwargs:
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        storage.new(self)
    else:
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
        for key, value in kwargs.items():
            if key in {'created_at', 'updated_at'}:
                value = datetime.strptime(value, date_format)
            if key != '__class__':
                setattr(self, key, value)