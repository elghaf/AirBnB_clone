#!/usr/bin/python3
"""Console module
"""

import cmd
import importlib
import json
import re
from typing import cast

from models import storage


class HBNBCommand(cmd.Cmd):
    """HBNB CLASS CLONE"""

    prompt = "(hbnb) "

    def do_quit(self, line):
        """Quit command"""
        return True

    def do_EOF(self, line):
        """Exist Ctrl + D"""
        print()
        return True


    def do_create(self, line):
        """creates a new object and saves it"""
        class_type = self.get_class_from_input(line)
        if class_type:
            class_types = class_type()
            class_types.save()
            print(class_types.id)

    def do_show(self, line):
        """prints the string of inst (name, id)
        """
        object_key = self.get_obj_key_from_input(line)

        if object_key:
            stored_instance = storage.all().get(object_key, None)

            if stored_instance:
                print(stored_instance)
            else:
                print("inst not found")

    def do_destroy(self, line):
        """deletes an instance
        """
        object_key = self.get_obj_key_from_input(line)

        if object_key:
            stored_instance = storage.all().pop(object_key, None)

            if stored_instance:
                storage.save()
            else:
                print("not found")

    def do_all(self, line):
        """prints all string representation inst the class name
        """
        arguments = line.split()

        if not arguments:
            result = storage.all().values()
        else:
            obj_cls = self.get_class_from_input(line)

            if obj_cls is None:
                return

            result = filter(lambda item: isinstance(item, obj_cls), storage.all().values())

        print([str(item) for item in result])

    def do_update(self, line):
        """updates an inst
        """
        object_key = self.get_obj_key_from_input(line)

        if not object_key:
            return

        stored_instance = storage.all().get(object_key)

        if not stored_instance:
            print("not found")
            return

        attribute_name, attribute_value = self.get_attribute_name_value_pair(line)

        if attribute_name is None or attribute_value is None:
            return

        if hasattr(stored_instance, attribute_name):
            attribute_type = type(getattr(stored_instance, attribute_name))
            attribute_value = cast(attribute_type, attribute_value)

        setattr(stored_instance, attribute_name, attribute_value)
        stored_instance.save()


    def do_count(self, line):
        """prints cts instance"""
        do_cont = self.get_class_from_input(line)

        if do_cont is None:
            return

        do_cots = sum(1 for item in storage.all().values() if isinstance(item, do_cont))
        print(do_cots)

    def get_obj_key_from_input(self, line):
        """parses and returns object key from input"""
        obj_cls = self.get_class_from_input(line)
        id_value = self.get_id_from_input(line)

        if obj_cls is None or id_value is None:
            return None

        return f"{obj_cls.__name__}.{id_value}"

    def get_class_from_input(self, line):
        """parses and returns class from input"""
        if line is None or len(line.strip()) == 0:
            print("** class name missing **")
            return None

        return self.get_class(line.split()[0])

    def get_id_from_input(self, line):
        """parses and returns id from input"""
        cmds = line.split()
        if len(cmds) < 2:
            print("** instance id missing **")
            return None
        return cmds[1]

    def get_attribute_name_value_pair(self, line):
        """parses and returns a tuple of attribute name and value"""
        cmds = line.split()

        attr_name = None if len(cmds) < 3 else cmds[2].strip('"')
        if attr_name is None:
            print("** attribute name missing **")
            return None, None

        attr_val = None if len(cmds) < 4 else cmds[3].strip('"')
        if attr_val is None:
            print("** value missing **")
            return attr_name, None

        return attr_name, attr_val

    def get_class(self, name):
        """ returns a class from models module using its name"""
        try:
            sub_module = re.sub('(?!^)([A-Z]+)', r'_\1', name).lower()
            module = importlib.import_module(f"models.{sub_module}")
            return getattr(module, name)
        except Exception:
            print("** class doesn't exist **")
            return None

    def default(self, line):
        if '.' not in line:
            return super().default(line)

        cls_name, func_name, id, args = self.parse_input(line)

        if cls_name is None:
            print("** class name missing **")
            return

        if func_name is None:
            print(
                "** incorrect function (all, count, show, destroy & update) **"
            )
            return

        id = id if id is not None else ""

        if func_name == "count":
            self.do_count(cls_name)
        elif func_name == "all":
            self.do_all(cls_name)
        elif func_name == "show":
            self.do_show(f"{cls_name} {id}")
        elif func_name == "destroy":
            self.do_destroy(f"{cls_name} {id}")
        elif func_name == "update":
            if isinstance(args, str):
                args = " ".join([id, args])
                self.do_update(f"{cls_name} {args}")
            elif isinstance(args, dict):
                for k, v in args.items():
                    self.do_update(f"{cls_name} {id} {k} {v}")

    def parse_input(self, input):
        args = input.split('.')
        if len(args) != 2:
            return None, None, None, None

        cls_name = args[0]
        valid_commands = ["all", "count", "show", "destroy", "update"]
        if '(' not in args[1] or ')' not in args[1]:
            return cls_name, None, None, None

        func_w_args = args[1].split("(")
        if len(func_w_args) == 0 or func_w_args[0] not in valid_commands:
            return cls_name, None, None, None
        func_name = func_w_args[0]
        f_args = func_w_args[1].strip(')')

        id_match = re.match(r'(^\"[\w-]+\")', f_args)
        if len(f_args) == 0 or id_match is None:
            return cls_name, func_name, None, None

        id = id_match.group()
        f_args = f_args.replace(id, "")
        id = id.strip('"')

        if len(f_args) == 0:
            return cls_name, func_name, id, ''

        dict_match = re.match(r'(\{.*\})', f_args.strip(", "))
        if dict_match is not None:
            dict_str = dict_match.group().replace("'", '"')
            return (
                cls_name, func_name, id, dict(json.loads(dict_str))
            )

        f_args = f_args.replace(',', ' ')
        return cls_name, func_name, id, str(f_args)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
