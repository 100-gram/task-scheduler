from flask import Blueprint, jsonify, abort, request
from controller.datamanager import DataManager
from config.config import json_response

"""
This api module

Api module to perform CRUD operations with Task entities
"""

api = Blueprint('api', __name__)


@api.route('/')
def index():
    return jsonify({'info': 'You can get info about api in doc/documentation.html'})


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
    storage = DataManager.load_from_file()
    if storage.change_task_status(task_id, not set_uncompleted):
        task = storage.get_by_id(task_id)
        return json_response({"task": task})
    else:
        abort(404, f"Couldn't find such task with id: {task_id}")
