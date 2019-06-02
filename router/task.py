from flask import abort
from flask_restful import Resource
from config.config import json_response, task_params_parser, storage_path
from controller.datamanager import DataManager

"""
Task restful api module 

Provide methods to manage with Task entity
"""


class Task(Resource):
    """
    Create instance of Task restful api route
    """
    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.data_manager = DataManager.load_from_file(storage_path)

    def get(self, task_id):
        """
        Api Method Path('/tasks/<int:task_id>'), method 'Get'
        Get Task by id

        :param task_id: id of searched Task
        :return: JSON Response with searched Task or error 404 if this task doesn`t exist
        """
        storage = self.data_manager
        task = storage.get_by_id(task_id)
        if task is False:
            return abort(404, f"Couldn't find such task with id: {task_id}")
        return json_response({"task": task})

    def delete(self, task_id):
        """
        Api Method Path('/tasks/<int:task_id>'), method 'DELETE'
        Delete Task by id

        :param task_id: id of deleted Task
        :return: empty 204 response if Task is deleted and error 404 if this task doesn`t exist
        """
        storage = self.data_manager
        if storage.delete_task(task_id):
            return '', 204
        else:
            abort(404, f"Couldn't find such task with id: {task_id}")

    def put(self, task_id):
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
        storage = self.data_manager
        task = task_params_parser().parse_args()
        try:
            if storage.update_task_info(task_id, task.name, task.description, task.date_start, task.duration):
                task = storage.get_by_id(task_id)
                return json_response({"task": task})
            else:
                abort(404, f"Couldn't find such task with id: {task_id}")
        except ValueError as e:
            return abort(400, str(e))
