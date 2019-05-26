from os import path
from sys import modules
from os import system, name

app_path = path.dirname(modules['__main__'].__file__)

storage_path = path.join(app_path, 'data', 'tasks.json')


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')
