#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage
           Args
              cls: The type of class to return
           Return: dict
        """
        if cls:
            ret_dict = {}
            all_objects = self.__objects
            for k in all_objects:
                clsname = k.partition('.')[0]
                if clsname == cls.__name__:
                    ret_dict[k] = self.__objects[k]
            return ret_dict
        else:
            return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj:
            self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Saves storage dictionary to file"""
        temp = {}
        for key, value in self.__objects.items():
            temp[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ delete an existing element
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]
            self.save()

    def close(self):
        """
        deserializing the JSON file to objects
        """
        self.reload()
