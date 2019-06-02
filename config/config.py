from os import path, system, name
from sys import modules
from flask import request, Response
from flask_restful import reqparse
import simplejson
import logging

"""
This module store some configuration data

Here provided path to storage file and some others helper functions
"""

app_path = path.dirname(modules['__main__'].__file__)

api_prefix = "/api/v1"

# storage_path = "/home/a_krava/projects/github/task-scheduler/data/tasks.json"
storage_path = path.join(app_path, 'data', 'tasks.json')


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


def disable_log(app):
    """
    Disable any output from Flask server

    :param app: instance of Flask application
    :return: None
    """
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.logger.disabled = True


def json_response(data, status=200):
    """
    Make flask response with json data and passed http status

    :param data: object or list. This data will be serialized to json string
    :param status: int. Http response code status
    :return: Response flask object, with application/json data
    """
    json = simplejson.dumps(data, indent=4, for_json=True)
    return Response(json, status=status, mimetype='application/json')


def task_params_parser():
    """
    Make dict with requests params of Task entity

    :return: dict. all information about task
    """
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, location='json', required=True)
    parser.add_argument('description', type=str, location='json', required=True)
    parser.add_argument('date_start', type=str, location='json', required=True)
    parser.add_argument('duration', type=int, location='json', required=True)
    return parser


def query_pagination_params_parser():
    """
     Make dict with requests params, which are used for pagination and filtering

    :return: dict. Here offset is int; limit is int; query is str
    """
    parser = reqparse.RequestParser()
    parser.add_argument('offset', type=int, location='json')
    parser.add_argument('limit', type=int, location='json')
    parser.add_argument('query', type=str, location='json')
    parser.add_argument('status', dest='tasks_status', type=str, location='json')
    return parser
