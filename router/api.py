from flask import Blueprint, jsonify, abort, request, current_app
from config.config import json_response, query_pagination_params, task_params_from_request, \
    check_task_entity, check_task_params
from model.task_status import TaskStatus

"""
This api module

Api module to perform CRUD operations with Task entities
"""

api = Blueprint('api', __name__)


@api.route('/')
def index():
    """
    Api Method Path('/'), method 'Get'

    :return: JSON response with info
    """
    return jsonify({'info': 'You can get info about api in doc/documentation.html'})


@api.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Api Method Path('/tasks'), method 'Get'
    Get all tasks

    Use params:
    - offset: count of skipping tasks
    - limit: count of Tasks in page
    - query: searched parameter

    :return: JSON response with tasks data
    """
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
    """
    Api Method Path('/tasks/<int:task_id>'), method 'Get'
    Get Task by id

    :param task_id: id of searched Task
    :return: JSON Response with searched Task or error 404 if this task doesn`t exist
    """
    storage = current_app.config["data_manager"]
    task = storage.get_by_id(task_id)
    if task is False:
        return abort(404, f"Couldn't find such task with id: {task_id}")
    return json_response({"task": task})


@api.route('/tasks/complete/<int:task_id>', methods=['PATCH'])
def complete_task(task_id):
    """
    Api Method Path('/tasks/complete/<int:task_id>'), method 'PATCH'
    Complete or incomplete Task by id

    Use params:
    - set_uncompleted: status of completing Task

    :param task_id: id of changed Task
    :return: JSON Response with completed/uncompleted Task or error 404 if this task doesn`t exist
    """
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
    """
    Api Method Path('/tasks'), method 'POST'
    Create Task

    Use params:
    - name: name of new Task
    - description: description of new Task
    - date_start: start date of new Task
    - duration: duration of new Task

    :return: JSON Response with created Task or error 400 if there aren`t all needed data or data is invalid
    """
    storage = current_app.config["data_manager"]
    if check_task_params():
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
    """
    Api Method Path('/tasks/<int:task_id>'), method 'DELETE'
    Delete Task by id

    :param task_id: id of deleted Task
    :return: empty 204 response if Task is deleted and error 404 if this task doesn`t exist
    """
    storage = current_app.config["data_manager"]
    if storage.delete_task(task_id):
        return '', 204
    else:
        abort(404, f"Couldn't find such task with id: {task_id}")


@api.route('/tasks/<int:task_id>', methods=['PUT'])
def update_item(task_id):
    """
    Api Method Path('/tasks/<int:task_id>'), method 'PUT'
    Update Task by id

    Use params:
    - name: name of updating Task
    - description: description of updating Task
    - date_start: start date of updating Task
    - duration: duration of updating Task

    :param task_id: id of updating Task
    :return: JSON Response with updated Task or error 400 if there aren`t all needed data or data is invalid
    and error 404 if this task doesn`t exist
    """
    storage = current_app.config["data_manager"]
    if check_task_params():
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
