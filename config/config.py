from os import path
from sys import modules

app_path = path.dirname(modules['__main__'].__file__)

storage_path = path.join(app_path, 'data', 'tasks.json')
