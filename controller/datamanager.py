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
    def __init__(self, next_id: int, tasks: [Task]):
        """
        Constructor for DataManager object

        :param next_id: id of task, that will be created next
        :param tasks: list of Task entities
        """
        self.next_id = next_id
        self.tasks = tasks

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
    def load_from_file(cls):
        """
        Create DataManager instance from file with JSON data


        :return:
        """
        data_str = open(storage_path, 'r').read()
        storage_obj = simplejson.loads(data_str)
        return DataManager.from_json(storage_obj)

    def save_to_file(self):
        with open(storage_path, 'w') as outfile:
            simplejson.dump(self, outfile, indent=4, for_json=True)

    def update_from_file(self):
        data_str = open(storage_path, 'r').read()
        storage_obj = simplejson.loads(data_str)
        self.next_id = storage_obj['next_id']
        self.tasks = DataManager.tasks_from_json(storage_obj['tasks'])

    def get_all(self, offset=0, limit=None, query=None):
        self.update_from_file()
        return DataManager.__paginate_and_search(self.tasks, offset, limit, query)

    def get_with_status(self, status: TaskStatus, offset=0, limit=None, query=None):
        self.update_from_file()
        filter_function = {
            TaskStatus.COMPLETED: lambda x: x.completed(),
            TaskStatus.UNCOMPLETED: lambda x: not x.completed(),
            TaskStatus.PLANNED: lambda x: not x.is_finished() and not x.is_running(),
            TaskStatus.RUNNING: lambda x: x.is_running(),
            TaskStatus.FINISHED: lambda x: x.is_finished(),
        }[status]
        result = list(filter(filter_function, self.tasks))
        return DataManager.__paginate_and_search(result, offset, limit, query, status)

    def get_by_id(self, task_id: int):
        self.update_from_file()
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                return self.tasks[i]
        return False

    def update_task(self, task_id: int, new_task: Task):
        self.update_from_file()
        new_task.task_id = task_id
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                self.tasks[i] = new_task
                self.save_to_file()
                return True
        return False

    def change_task_status(self, task_id: int, is_completed: bool):
        self.update_from_file()
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                self.tasks[i].is_completed = is_completed
                self.save_to_file()
                return True
        return False

    def update_task_info(self, task_id: int, name: str, description: str, date_start: str, duration: int):
        self.update_from_file()
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                self.tasks[i].name = name
                self.tasks[i].description = description
                self.tasks[i].date_start = parser.parse(date_start)
                self.tasks[i].date_end = parser.parse(date_start) + timedelta(seconds=duration)
                self.save_to_file()
                return True
        return False

    def delete_task(self, task_id: int):
        self.update_from_file()
        length = self.tasks.__len__()
        self.tasks = list(filter(lambda task: task.task_id != task_id, self.tasks))
        self.save_to_file()
        return length != self.tasks.__len__()

    def add_task(self, task: Task):
        self.update_from_file()
        task.task_id = self.next_id
        self.tasks.append(task)
        self.next_id += 1
        self.save_to_file()
        return task

    def create_task(self, name: str, description: str, date_start: str, duration: int):
        self.update_from_file()
        task = Task.create(self.next_id, name, description, date_start, duration)
        self.tasks.append(task)
        self.next_id += 1
        self.save_to_file()
        return task

    @staticmethod
    def __paginate_array(array, offset=0, limit=None):
        if isinstance(offset, int) and offset >= 0 and ((isinstance(limit, int) and limit > 0) or limit is None):
            return array[offset:(limit + offset if limit is not None else None)]
        return array

    @staticmethod
    def __search_filter(array: [Task], query=None):
        length = array.__len__()
        if not isinstance(query, str) or query.__len__() == 0:
            return array, length
        return list(filter(lambda x: re.search(query, x.name + x.description, re.IGNORECASE), array)), length

    @staticmethod
    def __paginate_and_search(array, offset=0, limit=None, query=None, status_filter=None):
        filtered, length = DataManager.__search_filter(array, query)
        tasks_result = DataManager.__paginate_array(filtered, offset, limit)
        return Response(tasks_result, offset, limit, query, length, status_filter)
