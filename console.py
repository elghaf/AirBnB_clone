#!/usr/bin/python3
import cmd



class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb)"

    def default(self, line: str):
        self._precmd(line)


if __name__== '__main__':
    HBNBCommand().cmdloop()