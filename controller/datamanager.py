from model.task import Task
from dateutil import parser
from datetime import timedelta
import simplejson
from config.config import storage_path


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
        new_str = open(storage_path, 'r').read()
        storage_obj = simplejson.loads(new_str)
        return DataManager.from_json(storage_obj)

    def save(self):
        with open(storage_path, 'w') as outfile:
            simplejson.dump(self, outfile, indent=4, for_json=True)

    def get_all(self):
        return self.tasks

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
