from model.task import Task
from config.config import storage_path
from model.task_status import TaskStatus
from model.response import Response
from dateutil import parser
from datetime import timedelta
import simplejson
import re

"""
This controller for json storage of Task entities

Provide all methods to manage with Task entities
"""


class DataManager:
    def __init__(self, next_id: int, tasks: [Task], file_path=None):
        """
        Constructor for DataManager object

        :param next_id: id of task, that will be created next
        :param tasks: list of Task entity;
        """
        self.next_id = next_id
        self.tasks = tasks
        self.storage_path = file_path if file_path is str else storage_path

    def __json__(self):
        """
        JSON serialization for DataManager object

        :return: dict with all inner fields
        """
        return {
            'next_id': self.next_id,
            'tasks': self.tasks,
        }

    for_json = __json__  # supported by simplejson

    @classmethod
    def from_json(cls, json_obj):
        """
        Creating DataManager object from JSON object

        :param json_obj: JSON object (dict)
        :return: instance of DataManager
        """
        return cls(json_obj['next_id'], DataManager.tasks_from_json(json_obj['tasks']))

    @classmethod
    def tasks_from_json(cls, storage_obj):
        """
        Deserialize Tasks from JSON object

        :param storage_obj: JSON serialized Tasks
        :return: list of Task entities
        """
        return list(map(lambda x: Task.from_json(x), storage_obj))

    @classmethod
    def load_from_file(cls, file_path: str):
        """
        Create DataManager instance from file with JSON data

        :param file_path: set explicitly file path of data storage
        :return:instance of DataManager
        """
        data_str = open(file_path, 'r').read()
        storage_obj = simplejson.loads(data_str)
        return DataManager.from_json(storage_obj)

    def set_storage_path(self, file_path: str):
        """
        Set storage path for data

        :param file_path: file path to json file
        :return: None
        """
        self.storage_path = file_path

    def save_to_file(self, file_path: str):
        """
        Save changes(tasks ans next_id) in data file

        :param file_path: set explicitly file path of data storage
        :return: None
        """
        with open(file_path, 'w') as outfile:
            simplejson.dump(self, outfile, indent=4, for_json=True)

    def update_from_file(self, file_path: str):
        """
        Get changes( tasks ans next_id) from data file

        :param file_path: set explicitly file path of data storage
        :return: None
        """
        data_str = open(file_path, 'r').read()
        storage_obj = simplejson.loads(data_str)
        self.next_id = storage_obj['next_id']
        self.tasks = DataManager.tasks_from_json(storage_obj['tasks'])

    def get_all(self, offset=0, limit=None, query=None):
        """
        Get all filtered and paginated tasks

        :param offset: count of skipping tasks
        :param limit: count of tasks in page
        :param query: search parameter
        :return: list of Task entities
        """
        self.update_from_file(self.storage_path)
        return DataManager.__paginate_and_search__(self.tasks, offset, limit, query)

    def get_with_status(self, status: TaskStatus, offset=0, limit=None, query=None):
        """
        Get all filtered and paginated tasks with selected status

        :param status: selected status of Task
        :param offset: count of skipping tasks
        :param limit: count of tasks in page
        :param query: search parameter
        :return: list of Task entities
        """
        self.update_from_file(self.storage_path)
        filter_function = {
            TaskStatus.COMPLETED: lambda x: x.completed(),
            TaskStatus.UNCOMPLETED: lambda x: not x.completed(),
            TaskStatus.PLANNED: lambda x: not x.is_finished() and not x.is_running(),
            TaskStatus.RUNNING: lambda x: x.is_running(),
            TaskStatus.FINISHED: lambda x: x.is_finished(),
        }[status]
        result = list(filter(filter_function, self.tasks))
        return DataManager.__paginate_and_search__(result, offset, limit, query, status)

    def get_by_id(self, task_id: int):
        """
        Get Task entity with selected id

        :param task_id: id of searched Task
        :return: Task entity if task with selected id exists else False
        """
        self.update_from_file(self.storage_path)
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                return self.tasks[i]
        return False

    def update_task(self, task_id: int, new_task: Task):
        """
        Update Task by id

        :param task_id: id of updating Task
        :param new_task: Task entity with updating info
        :return: True if entity was updated else False
        """
        self.update_from_file(self.storage_path)
        new_task.task_id = task_id
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                self.tasks[i] = new_task
                self.save_to_file(self.storage_path)
                return True
        return False

    def change_task_status(self, task_id: int, is_completed: bool):
        """
        Change Task status

        :param task_id: id of updating Task
        :param is_completed: Task status
        :return:True if entity was updated else False
        """
        self.update_from_file(self.storage_path)
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                self.tasks[i].is_completed = is_completed
                self.save_to_file(self.storage_path)
                return True
        return False

    def update_task_info(self, task_id: int, name: str, description: str, date_start: str, duration: int):
        """
        Update Task info

        :param task_id: id of updating Task
        :param name: updated name of Task
        :param description: updated description of Task
        :param date_start: updated start date of Task
        :param duration: updated duration of Task
        :return: True if entity was updated else False
        """
        self.update_from_file(self.storage_path)
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                self.tasks[i].name = name
                self.tasks[i].description = description
                self.tasks[i].date_start = parser.parse(date_start)
                self.tasks[i].date_end = parser.parse(date_start) + timedelta(seconds=duration)
                self.save_to_file(self.storage_path)
                return True
        return False

    def delete_task(self, task_id: int):
        """
        Delete Task

        :param task_id: id of deleted Task
        :return: True if entity was deleted else False
        """
        self.update_from_file(self.storage_path)
        length = self.tasks.__len__()
        self.tasks = list(filter(lambda task: task.task_id != task_id, self.tasks))
        self.save_to_file(self.storage_path)
        return length != self.tasks.__len__()

    def add_task(self, task: Task):
        """
        Add new Task to storage

        :param task: new Task entity
        :return: added Task entity
        """
        self.update_from_file(self.storage_path)
        task.task_id = self.next_id
        self.tasks.append(task)
        self.next_id += 1
        self.save_to_file(self.storage_path)
        return task

    def create_task(self, name: str, description: str, date_start: str, duration: int):
        """
        Create new Task

        :param name: name of new Task
        :param description: description of new Task
        :param date_start: start date of new Task
        :param duration: duration of new Task
        :return: created Task entity
        """
        self.update_from_file(self.storage_path)
        task = Task.create(self.next_id, name, description, date_start, duration)
        self.tasks.append(task)
        self.next_id += 1
        self.save_to_file(self.storage_path)
        return task

    @staticmethod
    def __paginate_array__(array, offset=0, limit=None):
        """
        Paginate list of Tasks

        :param array: list of Tasks
        :param offset: count of skipping tasks
        :param limit: count of Tasks in page
        :return: paginated list of Tasks
        """
        if isinstance(offset, int) and offset >= 0 and ((isinstance(limit, int) and limit > 0) or limit is None):
            return array[offset:(limit + offset if limit is not None else None)]
        return array

    @staticmethod
    def __search_filter__(array: [Task], query=None):
        """
        Search Tasks in list

        :param array: list of Tasks
        :param query: searched parameter
        :return: list of Tasks that consist searched parameter
        """
        length = array.__len__()
        if not isinstance(query, str) or query.__len__() == 0:
            return array, length
        return list(filter(lambda x: re.search(query, x.name + x.description, re.IGNORECASE), array)), length

    @staticmethod
    def __paginate_and_search__(array, offset=0, limit=None, query=None, status_filter=None):
        """
        Paginate list of Tasks and Search Tasks in it

        :param array: list of Tasks
        :param offset: count of skipping tasks
        :param limit: count of Tasks in page
        :param query: searched parameter
        :param status_filter: searched Task status
        :return: paginated list of Tasks that consist searched parameter
        """
        filtered, length = DataManager.__search_filter__(array, query)
        tasks_result = DataManager.__paginate_array__(filtered, offset, limit)
        return Response(tasks_result, offset, limit, query, length, status_filter)
