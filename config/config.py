from os import path, system, name
from sys import modules
from flask import request, Response
import simplejson

"""
This module store some configuration data

Here provided path to storage file and some others helper functions
"""

app_path = path.dirname(modules['__main__'].__file__)

storage_path = "/home/a_krava/projects/github/task-scheduler/data/tasks.json"
# storage_path = path.join(app_path, 'data', 'tasks.json')


def clear():
    """
    Clear console function os-independent

    :return: NoneType
    """
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def shutdown_server():
    """
    Shutdown flask server

    :return: NoneType
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def json_response(data, status=200):
    """
    Make flask response with json data and passed http status

    :param data: object or list. This data will be serialized to json string
    :param status: int. Http response code status
    :return: Response flask object, with application/json data
    """
    json = simplejson.dumps(data, indent=4, for_json=True)
    return Response(json, status=status, mimetype='application/json')


def query_pagination_params():
    """
    Make dict with requests params, which are used for pagination and filtering

    :return: dict. Here offset is int (by default 0); limit is int (by default None); query is str
    """
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    return {
        'offset': int(offset) if offset is not None and offset.isdigit() else 0,
        'limit': int(limit) if limit is not None and limit.isdigit() else None,
        'query': request.args.get('query')
    }


def task_params_from_request():
    """
    Make dict with requests params of Task entity

    :return: dict. all information about task
    """
    return {
        'name': request.json['name'],
        'description': request.json['description'],
        'date_start': request.json['date_start'],
        'duration': request.json['duration']
    }


def check_task_entity(task):
    return task.name and isinstance(task.name, str) and task.description and isinstance(task.description, str) \
           and task.date_start and isinstance(task.date_start, str) and task.duration \
           and isinstance(task.duration, int)


def check_pagination_params():
    return not request.json or 'name' not in request.json or 'description' not in request.json \
           or 'date_start' not in request.json or 'duration' not in request.json
