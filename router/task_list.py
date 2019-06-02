from flask import abort
from flask_restful import Resource
from model.task_status import TaskStatus
from config.config import json_response, task_params_parser, query_pagination_params_parser
from controller.datamanager import DataManager


class TaskList(Resource):
    def __init__(self, *args, **kwargs):
        super(TaskList, self).__init__(*args, **kwargs)
        self.data_manager = DataManager.load_from_file()

    def get(self):
        """
        Api Method Path('/tasks'), method 'Get'
        Get all tasks

        Use params:
        - offset: count of skipping tasks
        - limit: count of Tasks in page
        - query: searched parameter

        :return: JSON response with tasks data
        """
        storage = self.data_manager
        params = query_pagination_params_parser().parse_args()
        try:
            tasks_status = TaskStatus[params['tasks_status']]
        except KeyError:
            tasks_status = None
        if isinstance(tasks_status, TaskStatus):
            data = storage.get_with_status(tasks_status, params['offset'], params['limit'], params['query'])
        else:
            data = storage.get_all(params['offset'], params['limit'], params['query'])
        return json_response(data)

    def post(self):
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
        storage = self.data_manager
        task = task_params_parser().parse_args()
        try:
            task = storage.create_task(task.name, task.description, task.date_start, task.duration)
        except ValueError as e:
            return abort(400, str(e))
        return json_response({"task": task}, 201)
