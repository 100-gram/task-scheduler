from os import path, system, name
from sys import modules
from flask import request

app_path = path.dirname(modules['__main__'].__file__)

storage_path = path.join(app_path, 'data', 'tasks.json')


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
