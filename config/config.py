from os import path, system, name
from sys import modules
from flask import request, Response
import simplejson

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


def json_response(data, status=200):
    json = simplejson.dumps(data, indent=4, for_json=True)
    return Response(json, status=status, mimetype='application/json')


def query_pagination_params():
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    return {
        'offset': int(offset) if offset is not None and offset.isdigit() else 0,
        'limit': int(limit) if limit is not None and limit.isdigit() else None,
        'query': request.args.get('query')
    }
