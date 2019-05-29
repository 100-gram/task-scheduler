from flask import Blueprint, jsonify, abort, request, current_app
from config.config import json_response, query_pagination_params, task_params_from_request, \
    check_task_entity, check_pagination_params
from model.task_status import TaskStatus

"""
This api module

Api module to perform CRUD operations with Task entities
"""

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
        data = storage.get_with_status(tasks_status, params['offset'], params['limit'], params['query'])
    else:
        data = storage.get_all(params['offset'], params['limit'], params['query'])
    return json_response(data)


@api.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    storage = current_app.config["data_manager"]
    task = storage.get_by_id(task_id)
    if task is False:
        return abort(404, f"Couldn't find such task with id: {task_id}")
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
        abort(404, f"Couldn't find such task with id: {task_id}")


@api.route('/tasks', methods=['POST'])
def create_task():
    storage = current_app.config["data_manager"]
    if check_pagination_params():
        abort(400, "Please, pass all needed data to create task")
    task = task_params_from_request()
    if check_task_entity(task):
        try:
            task = storage.create_task(task.name, task.description, task.date_start, task.duration)
        except ValueError as e:
            return abort(400, str(e))
        return json_response({"task": task}, 201)
    else:
        abort(400, "Invalid data, couldn't add")


@api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_item(task_id):
    storage = current_app.config["data_manager"]
    if storage.delete_task(task_id):
        return '', 204
    else:
        abort(404, f"Couldn't find such task with id: {task_id}")


@api.route('/tasks/<int:task_id>', methods=['PUT'])
def update_item(task_id):
    storage = current_app.config["data_manager"]
    if check_pagination_params():
        abort(400, "Please, pass all needed data to update task")
    task = task_params_from_request()
    if not check_task_entity(task):
        return abort(400, "Invalid data, couldn't update")
    try:
        if storage.update_task_info(task_id, task.name, task.description, task.date_start, task.duration):
            task = storage.get_by_id(task_id)
            return json_response({"task": task})
        else:
            abort(404, f"Couldn't find such task with id: {task_id}")
    except ValueError as e:
        return abort(400, str(e))
