#!/usr/bin/python3
"""Modules documentation"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.review import Review
import json
import re
from models import storage

import re
from typing import Type


import re
from typing import Type

class HBNBCommand(cmd.Cmd):
    """Interactive command-line interface for HBNB project."""

    prompt = '(hbnb) '

    def precmd(self, argument):
        """Hook method executed just before the command is processed."""
        if re.search(".+.all\(\)", argument) or argument == ".all()":
            return f"all {argument[:-6]}"
        elif re.search(".+.count\(\)", argument) or argument == ".count()":
            return f"count {argument[:-8]}"
        return argument

    def do_quit(self, argument):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, argument):
        """Handles the end-of-file (EOF) condition."""
        print()
        return True

    def emptyline(self):
        """Method called when an empty line is entered."""
        pass

    def do_create(self, argument):
        """Creates a new instance, saves it, and prints the id."""
        class_mapping = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'City': City, 'State': State, 'Amenity': Amenity, 'Review': Review
        }

        arguments = argument.split()

        if len(arguments) < 1:
            print("** class name missing **")
            return

        class_name = arguments[0]

        if class_name not in class_mapping:
            print("** class doesn't exist **")
            return

        new_instance = class_mapping[class_name]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, argument):
        """Prints the string representation of an instance."""
        class_mapping = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'City': City, 'State': State, 'Amenity': Amenity, 'Review': Review
        }

        arguments = argument.split()

        if len(arguments) < 1:
            print("** class name missing **")
            return

        class_name = arguments[0]

        if class_name not in class_mapping:
            print("** class doesn't exist **")
            return

        if len(arguments) < 2:
            print("** instance id missing **")
            return

        storage.reload()

        key_to_find = "{}.{}".format(class_name, arguments[1])

        for key, value in storage.all().items():
            if key == key_to_find:
                print(value)
                return

        print("** no instance found **")

    def do_destroy(self, argument):
        """Deletes an instance based on the class name and id."""
        class_mapping = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'City': City, 'State': State, 'Amenity': Amenity, 'Review': Review
        }

        arguments = argument.split()

        if len(arguments) < 1:
            print("** class name missing **")
            return

        class_name = arguments[0]

        if class_name not in class_mapping:
            print("** class doesn't exist **")
            return

        if len(arguments) < 2:
            print("** instance id missing **")
            return

        storage.reload()
        key_to_delete = "{}.{}".format(class_name, arguments[1])

        instances = storage.all()

        if key_to_delete in instances:
            del instances[key_to_delete]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, argument):
        """Prints all string representation of all instances."""
        class_mapping = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'City': City, 'State': State, 'Amenity': Amenity, 'Review': Review
        }

        storage.reload()
        instances_list = []

        if not argument:
            for value in storage.all().values():
                instances_list.append(str(value))

        if len(argument.split()) == 1:
            if argument.split()[0] in class_mapping:
                for value in storage.all().values():
                    if value.__class__.__name__ == argument.split()[0]:
                        instances_list.append(str(value))
            else:
                print("** class doesn't exist **")
                return

        print(instances_list)

    def do_count(self, argument):
        """Prints the count of instances based on the class name."""
        class_mapping = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'City': City, 'State': State, 'Amenity': Amenity, 'Review': Review
        }

        storage.reload()
        instances_list = []

        if not argument:
            for value in storage.all().values():
                instances_list.append(str(value))

        if len(argument.split()) == 1:
            if argument.split()[0] in class_mapping:
                for value in storage.all().values():
                    if value.__class__.__name__ == argument.split()[0]:
                        instances_list.append(str(value))
            else:
                print("** class doesn't exist **")
                return

        print(len(instances_list))

    def do_update(self, argument):
        """Updates an instance based on the class name and id."""
        class_mapping = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'City': City, 'State': State, 'Amenity': Amenity, 'Review': Review
        }

        arguments = argument.split()

        if len(arguments) < 1:
            print("** class name missing **")
            return

        class_name = arguments[0]

        if class_name not in class_mapping:
            print("** class doesn't exist **")
            return

        if len(arguments) < 2:
            print("** instance id missing **")
            return

        if len(arguments) < 3:
            print("** attribute name missing **")
            return

        storage.reload()
        instances = storage.all()

        key = "{}.{}".format(class_name, arguments[1])

        if key not in instances:
            print("** no instance found **")
            return

        if len(arguments) < 4:
            print("** value missing **")
            return

        instance = instances[key]
        attribute_name = arguments[2]
        attribute_value = arguments[3]

        if not hasattr(instance, attribute_name):
            setattr(instance, attribute_name, attribute_value)

        setattr(instance, attribute_name,
                type(getattr(instance, attribute_name))(attribute_value))

        instance.save()



if __name__ == '__main__':
    HBNBCommand().cmdloop()
