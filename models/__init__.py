#!/usr/bin/python3
"""create a unique FileStorage instance for your application"""
from os import environ
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.base_model import BaseModel
from models.user import User
from models.state import State


storage_type = environ.get('HBNB_TYPE_STORAGE')
if storage_type == "db":
    storage = DBStorage()
else:
    storage = FileStorage()
storage.reload()
