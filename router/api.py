from flask import Blueprint, make_response, jsonify, abort, request
from model.datamanager import DataManager
import simplejson

api = Blueprint('api/v1/', __name__)


@api.route('/')
def index():
    return jsonify({'info': 'get info about api docs somewhere'})


@api.route('/tasks', methods=['GET'])
def get_tasks():
    DataManager.get_all()
    return simplejson.dumps({"tasks": DataManager.get_all()}, indent=4, for_json=True)


@api.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    item = list(filter(lambda t: t.task_id == task_id, DataManager.get_all()))
    if len(item) == 0:
        abort(404)
    return simplejson.dumps({"task": item}, indent=4, for_json=True)


@api.route('/tasks/complete/<int:task_id>', methods=['GET'])
def complete_task(task_id):
    if DataManager.complete_task(task_id):
        item = list(filter(lambda t: t.task_id == task_id, DataManager.get_all()))
        return simplejson.dumps({"task": item}, indent=4, for_json=True)
    else:
        abort(404)


@api.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'name' not in request.json or 'description' not in request.json \
            or 'date_start' not in request.json or'duration' not in request.json:
        abort(400)
    _name = request.json['name']
    _description = request.json['description']
    _date_start = request.json['date_start']
    _duration = request.json['duration']
    if _name and _description and _date_start and _duration:
        task = DataManager.create_task(_name, _description, _date_start, _duration)
        return simplejson.dumps({"task": task}, indent=4, for_json=True), 201
    else:
        abort(400)


@api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_item(task_id):
    if DataManager.delete_task(task_id):
        return jsonify({'result': True})
    else:
        return jsonify({'result': False})


@api.route('/tasks/<int:task_id>', methods=['PUT'])
def update_item(task_id):
    if not request.json or 'name' not in request.json or 'description' not in request.json \
            or 'date_start' not in request.json or 'duration' not in request.json:
        abort(400)
    _name = request.json['name']
    _description = request.json['description']
    _date_start = request.json['date_start']
    _duration = request.json['duration']
    if _name and _description and _date_start and _duration:
        if DataManager.update_task_info(task_id, _name, _description, _date_start, _duration):
            item = list(filter(lambda t: t.task_id == task_id, DataManager.get_all()))
            return simplejson.dumps({"task": item}, indent=4, for_json=True), 200
        else:
            abort(404)
    else:
        abort(400)