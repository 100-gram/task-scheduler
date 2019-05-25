from model.task import Task
from dateutil import parser
from datetime import timedelta
import simplejson
import os
import sys

storage_path = os.path.dirname(sys.modules['__main__'].__file__) + '\\data\\tasks.json'


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
        obj = cls(json_obj['next_id'], DataManager.tasks_from_json(json_obj['tasks']))
        return obj

    def save(self):
        with open(storage_path, 'w') as outfile:
            simplejson.dump(self, outfile, indent=4, for_json=True)

    @classmethod
    def get_all(cls):
        new_str = open(storage_path, 'r').read()
        storage_obj = simplejson.loads(new_str)
        return DataManager.tasks_from_json(storage_obj['tasks'])

    @classmethod
    def create(cls):
        new_str = open(storage_path, 'r').read()
        storage_obj = simplejson.loads(new_str)
        return DataManager.from_json(storage_obj)

    @classmethod
    def update_task(cls, task_id: int, new_task):
        storage = DataManager.create()
        new_task.task_id = task_id
        for i, task in enumerate(storage.tasks):
            if task.task_id == task_id:
                storage.tasks[i] = new_task
        storage.save()

    @classmethod
    def update_task_info(cls, task_id: int, name: str, description: str, date_start, duration: int, is_complited: bool):
        storage = DataManager.create()
        for i, task in enumerate(storage.tasks):
            if task.task_id == task_id:
                storage.tasks[i].name = name
                storage.tasks[i].description = description
                storage.tasks[i].date_start = parser.parse(date_start)
                storage.tasks[i].date_end = parser.parse(date_start) + timedelta(minutes=duration)
                storage.tasks[i].is_complited = is_complited
        storage.save()

    @classmethod
    def delete_task(cls, task_id: int):
        storage = DataManager.create()
        storage.tasks = list(filter(lambda task: task.task_id != task_id, storage.tasks))
        storage.save()

    @classmethod
    def complete_task(cls, task_id: int):
        storage = DataManager.create()
        for task in storage.tasks:
            if task.task_id == task_id:
                task.is_complited = True
        storage.save()


    @classmethod
    def add_task(cls, task):
        storage = DataManager.create()
        task.task_id = storage.next_id
        storage.tasks.append(task)
        storage.next_id += 1
        storage.save()

    @classmethod
    def create_task(cls, name: str, description: str, date_start, duration: int):
        storage = DataManager.create()
        task = Task.create(storage.next_id, name, description, date_start, duration)
        storage.tasks.append(task)
        storage.next_id += 1
        storage.save()

    @classmethod
    def tasks_from_json(cls, storage_obj):
        tasks = []
        for val in storage_obj:
            tasks.append(Task.from_json(val))
        return tasks
