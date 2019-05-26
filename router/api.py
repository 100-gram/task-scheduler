from flask import Blueprint, jsonify, abort, request, current_app
from config.config import json_response, query_pagination_params
from model.task_status import TaskStatus

api = Blueprint('api', __name__)


@api.route('/')
def index():
    return jsonify({'info': 'You can get info about api in doc/documentation.html'})


@api.route('/tasks', methods=['GET'])
def get_tasks():
    storage = current_app.config["data_manager"]
    params = query_pagination_params()
    tasks_status = request.args.get('status')
    try:
        tasks_status = TaskStatus[tasks_status]
    except KeyError:
        tasks_status = None
    if isinstance(tasks_status, TaskStatus):
        data = storage.get_all(params['offset'], params['limit'], params['query'])
    else:
        data = storage.get_with_status(tasks_status, params['offset'], params['limit'], params['query'])
    return json_response(data)


@api.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    storage = current_app.config["data_manager"]
    task = storage.get_by_id(task_id)
    if task is False:
        return abort(404, "Couldn't find such task with id: " + task_id)
    return json_response({"task": task})


@api.route('/tasks/complete/<int:task_id>', methods=['PATCH'])
def complete_task(task_id):
    if request.json and 'set_uncompleted' in request.json and request.json['set_uncompleted'] is True:
        set_uncompleted = True
    else:
        set_uncompleted = False
    storage = current_app.config["data_manager"]
    if storage.change_task_status(task_id, not set_uncompleted):
        task = storage.get_by_id(task_id)
        return json_response({"task": task})
    else:
        abort(404, "Couldn't find such task with id: " + task_id)


@api.route('/tasks', methods=['POST'])
def create_task():
    storage = current_app.config["data_manager"]
    if not request.json or 'name' not in request.json or 'description' not in request.json \
            or 'date_start' not in request.json or'duration' not in request.json:
        abort(400, "Please, pass all needed data to update task")
    _name = request.json['name']
    _description = request.json['description']
    _date_start = request.json['date_start']
    _duration = request.json['duration']
    if _name and _description and _date_start and _duration:
        task = storage.create_task(_name, _description, _date_start, _duration)
        return json_response({"task": task}, 201)
    else:
        abort(400, "Invalid data, couldn't add")


@api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_item(task_id):
    storage = current_app.config["data_manager"]
    if storage.delete_task(task_id):
        return '', 204
    else:
        abort(404, "Couldn't find such task with id: " + task_id)


@api.route('/tasks/<int:task_id>', methods=['PUT'])
def update_item(task_id):
    storage = current_app.config["data_manager"]
    if not request.json or 'name' not in request.json or 'description' not in request.json \
            or 'date_start' not in request.json or 'duration' not in request.json:
        abort(400, "Please, pass all needed data to update task")
    _name = request.json['name']
    _description = request.json['description']
    _date_start = request.json['date_start']
    _duration = request.json['duration']
    if _name and _description and _date_start and _duration:
        if storage.update_task_info(task_id, _name, _description, _date_start, _duration):
            task = storage.get_by_id(task_id)
            return json_response({"task": task})
        else:
            abort(404, "Couldn't find such task with id: " + task_id)
    else:
        abort(400, "Invalid data, couldn't update")
