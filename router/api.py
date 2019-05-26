from flask import Blueprint, Response, jsonify, abort, request, current_app
from controller.datamanager import DataManager
import simplejson

api = Blueprint('api', __name__)


@api.route('/')
def index():
    return jsonify({'info': 'get info about api docs somewhere'})


@api.route('/tasks', methods=['GET'])
def get_tasks():
    storage = current_app.config["data_manager"]
    data = simplejson.dumps({"tasks": storage.get_all()}, indent=4, for_json=True)
    return Response(data, status=200, mimetype='application/json')


@api.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    storage = current_app.config["data_manager"]
    item = list(filter(lambda t: t.task_id == task_id, storage.get_all()))
    if len(item) == 0:
        abort(404)
    data = simplejson.dumps({"task": item}, indent=4, for_json=True)
    return Response(data, status=200, mimetype='application/json')


@api.route('/tasks/complete/<int:task_id>', methods=['GET'])
def complete_task(task_id):
    storage = current_app.config["data_manager"]
    if storage.complete_task(task_id):
        item = list(filter(lambda t: t.task_id == task_id, storage.get_all()))
        data = simplejson.dumps({"task": item}, indent=4, for_json=True)
        return Response(data, status=200, mimetype='application/json')
    else:
        abort(404)


@api.route('/tasks', methods=['POST'])
def create_task():
    storage = current_app.config["data_manager"]
    if not request.json or 'name' not in request.json or 'description' not in request.json \
            or 'date_start' not in request.json or'duration' not in request.json:
        abort(400)
    _name = request.json['name']
    _description = request.json['description']
    _date_start = request.json['date_start']
    _duration = request.json['duration']
    if _name and _description and _date_start and _duration:
        task = storage.create_task(_name, _description, _date_start, _duration)
        data = simplejson.dumps({"task": task}, indent=4, for_json=True)
        return Response(data, status=201, mimetype='application/json')
    else:
        abort(400)


@api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_item(task_id):
    storage = current_app.config["data_manager"]
    if storage.delete_task(task_id):
        return jsonify({'result': True})
    else:
        return jsonify({'result': False})


@api.route('/tasks/<int:task_id>', methods=['PUT'])
def update_item(task_id):
    storage = current_app.config["data_manager"]
    if not request.json or 'name' not in request.json or 'description' not in request.json \
            or 'date_start' not in request.json or 'duration' not in request.json:
        abort(400)
    _name = request.json['name']
    _description = request.json['description']
    _date_start = request.json['date_start']
    _duration = request.json['duration']
    if _name and _description and _date_start and _duration:
        if storage.update_task_info(task_id, _name, _description, _date_start, _duration):
            item = list(filter(lambda t: t.task_id == task_id, storage.get_all()))
            data = simplejson.dumps({"task": item}, indent=4, for_json=True)
            return Response(data, status=200, mimetype='application/json')
        else:
            abort(404)
    else:
        abort(400)
