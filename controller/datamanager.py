from model.task import Task
from config.config import storage_path
from dateutil import parser
from datetime import timedelta
import simplejson
import re


class DataManager:
    def __init__(self, next_id: int, tasks: [Task]):
        self.next_id = next_id
        self.tasks = tasks

    def __json__(self):
        return {
            'next_id': self.next_id,
            'tasks': self.tasks,
        }

    for_json = __json__  # supported by simplejson

    @classmethod
    def from_json(cls, json_obj):
        return cls(json_obj['next_id'], DataManager.tasks_from_json(json_obj['tasks']))

    @classmethod
    def tasks_from_json(cls, storage_obj):
        return list(map(lambda x: Task.from_json(x), storage_obj))

    @classmethod
    def load_from_file(cls):
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
        self.tasks = storage_obj['tasks']

    def get_all(self, offset=0, limit=None, query=None):
        self.update_from_file()
        return DataManager.__paginate_and_search(self.tasks, offset, limit, query)

    def get_completed(self, offset=0, limit=None, query=None, is_complited=True):
        self.update_from_file()
        completed = list(filter(
            lambda x: is_complited is True and x.is_complited() or is_complited is False and not x.is_complited(),
            self.tasks
        ))
        return DataManager.__paginate_and_search(completed, offset, limit, query)

    def get_finished(self, offset=0, limit=None, query=None):
        self.update_from_file()
        finished = list(filter(lambda x: x.is_finished(), self.tasks))
        return DataManager.__paginate_and_search(finished, offset, limit, query)

    def get_running(self, offset=0, limit=None, query=None):
        self.update_from_file()
        running = list(filter(lambda x: x.is_running(), self.tasks))
        return DataManager.__paginate_and_search(running, offset, limit, query)

    def update_task(self, task_id: int, new_task):
        new_task.task_id = task_id
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                self.tasks[i] = new_task
                self.save()
                return True
        return False

    def update_task_info(self, task_id: int, name: str, description: str, date_start, duration: int):
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                self.tasks[i].name = name
                self.tasks[i].description = description
                self.tasks[i].date_start = parser.parse(date_start)
                self.tasks[i].date_end = parser.parse(date_start) + timedelta(minutes=duration)
                self.save()
                return True
        return False

    def delete_task(self, task_id: int):
        len = self.tasks.__len__()
        self.tasks = list(filter(lambda task: task.task_id != task_id, self.tasks))
        self.save()
        return len != self.tasks.__len__()

    def complete_task(self, task_id: int):
        for task in self.tasks:
            if task.task_id == task_id:
                task.is_completed = True
                self.save()
                return True
        return False

    def add_task(self, task: Task):
        task.task_id = self.next_id
        self.tasks.append(task)
        self.next_id += 1
        self.save()
        return task

    def create_task(self, name: str, description: str, date_start, duration: int):
        task = Task.create(self.next_id, name, description, date_start, duration)
        self.tasks.append(task)
        self.next_id += 1
        self.save()
        return task

    @staticmethod
    def __paginate_array(array, offset=0, limit=None):
        return array[offset:(limit + offset if limit is not None else None)]

    @staticmethod
    def __search_filter(array: [Task], query=None):
        if query is None:
            return array
        return list(filter(lambda x: re.search(query, x.name + x.description, re.IGNORECASE), array))

    @staticmethod
    def __paginate_and_search(array, offset=0, limit=None, query=None):
        filtered = DataManager.__search_filter(array, query)
        return DataManager.__paginate_array(filtered, offset, limit)
