from model.task import Task
from config.config import storage_path, test_suits_folder_path
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
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit1.json")
        >>> a.__json__().__str__() == open(test_suits_folder_path + "/test_suit1.txt", 'r').read()
        True
        """
        return {
            'next_id': self.next_id,
            'tasks': DataManager.tasks_to_json(self.tasks),
        }

    for_json = __json__  # supported by simplejson

    @classmethod
    def from_json(cls, json_obj):
        """
        Creating DataManager object from JSON object

        :param json_obj: JSON object (dict)
        :return: instance of DataManager
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit1.json")
        >>> b = DataManager.from_json(a.__json__())
        >>> b.next_id
        2
        >>> b.tasks.__len__()
        1
        """
        return cls(json_obj['next_id'], DataManager.tasks_from_json(json_obj['tasks']))

    @staticmethod
    def tasks_from_json(storage_obj):
        """
        Deserialize Tasks from JSON object

        :param storage_obj: JSON serialized Tasks
        :return: list of Task entities
        >>> data_str = open(test_suits_folder_path + "/test_suit1.json", 'r').read()
        >>> storage_obj = simplejson.loads(data_str)['tasks']
        >>> a = DataManager.tasks_from_json(storage_obj)[0].__json__()
        >>> a['name']
        'Name'
        >>> a['date_start']
        '1999-08-28T21:03:05'
        """
        return list(map(lambda x: Task.from_json(x), storage_obj))

    @staticmethod
    def tasks_to_json(tasks):
        """
        Deserialize Tasks from JSON object

        :param tasks: JSON serialized Tasks
        :return: list of Task entities
        >>> arr = [Task(1, "Name", "nothing", parser.parse("1999-08-28T21:03:05"), \
            parser.parse("1999-08-28T05:55:23"), True)]
        >>> a = DataManager.tasks_to_json(arr)[0]
        >>> a['name']
        'Name'
        >>> a['date_start']
        '1999-08-28T21:03:05'
        >>> a['id']
        1
        """
        return list(map(lambda x: x.__json__(), tasks))

    @classmethod
    def load_from_file(cls, file_path: str):
        """
        Create DataManager instance from file with JSON data

        :param file_path: set explicitly file path of data storage
        :return: instance of DataManager
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit1.json")
        >>> a.next_id
        2
        >>> a.tasks.__len__()
        1
        """
        data_str = open(file_path, 'r').read()
        storage_obj = simplejson.loads(data_str)
        instance = DataManager.from_json(storage_obj)
        instance.storage_path = file_path
        return instance

    def set_storage_path(self, file_path: str):
        """
        Set storage path for data

        :param file_path: file path to json file
        :return: None
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit1.json")
        >>> prev = a.storage_path
        >>> a.set_storage_path("/path")
        >>> a.storage_path == "/path" and a.storage_path != prev
        True
        """
        self.storage_path = file_path

    def save_to_file(self, file_path: str):
        """
        Save changes(tasks ans next_id) in data file

        :param file_path: set explicitly file path of data storage
        :return: None
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit1.json")
        >>> a.save_to_file(test_suits_folder_path + "/test_suit2.json")
        >>> b = open(test_suits_folder_path + "/test_suit1.json", 'r').read()
        >>> c = open(test_suits_folder_path + "/test_suit2.json", 'r').read()
        >>> b == c
        True
        """
        with open(file_path, 'w') as outfile:
            simplejson.dump(self, outfile, indent=4, for_json=True)

    def update_from_file(self, file_path: str):
        """
        Get changes( tasks ans next_id) from data file

        :param file_path: set explicitly file path of data storage
        :return: None
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit1.json")
        >>> a.save_to_file(test_suits_folder_path + "/test_suit2.json")
        >>> a.change_task_status(1, False)
        True
        >>> b = DataManager.load_from_file(test_suits_folder_path + "/test_suit2.json")
        >>> a.tasks[0] != b.tasks[0]
        True
        >>> a.update_from_file(test_suits_folder_path + "/test_suit2.json")
        >>> a.tasks[0] == b.tasks[0]
        True
        >>> a.change_task_status(1, True)
        True
        >>> a.save_to_file(test_suits_folder_path + "/test_suit1.json")
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
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit1.json")
        >>> f = a.get_all().tasks
        >>> task = Task(1, "Name", "nothing", parser.parse("1999-08-28T21:03:05"), \
            parser.parse("1999-08-28T05:55:23"), True)
        >>> f[0] == task
        True
        >>> a.get_all(offset=1).tasks.__len__()
        0
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
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit1.json")
        >>> a.get_with_status(status=TaskStatus.UNCOMPLETED).tasks
        []
        >>> a.get_with_status(status=TaskStatus.COMPLETED).tasks.__len__()
        1
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
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit1.json")
        >>> task = Task(1, "Name", "nothing", parser.parse("1999-08-28T21:03:05"), \
            parser.parse("1999-08-28T05:55:23"), True)
        >>> a.get_by_id(1) == task
        True
        >>> a.get_by_id(-1)
        False
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
        :return: True if entity was updated else
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit3.json")
        >>> task = Task(1, "TEST val", "nothing", parser.parse("1999-08-28T21:03:05"), \
            parser.parse("1999-08-28T05:55:23"), True)
        >>> a.update_task(1, task)
        True
        >>> a.get_by_id(1) == task
        True
        >>> task.name = "TEst N2"
        >>> a.update_task(1, task)
        True
        >>> a.get_by_id(1) == task
        True
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
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit3.json")
        >>> a.change_task_status(1, False)
        True
        >>> a.get_by_id(1).completed()
        False
        >>> a.change_task_status(1, True)
        True
        >>> a.get_by_id(1).completed()
        True
        >>> a.change_task_status(-23, True)
        False
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
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit4.json")
        >>> temp = a.get_by_id(1)
        >>> a.update_task_info(1, "tEsT", "-.-", "2018", 3600)
        True
        >>> task = Task(1, "tEsT", "-.-", parser.parse("2018-06-03T00:00:00"), \
            parser.parse("2018-06-03T01:00:00"), True)
        >>> a.get_by_id(1) == task
        True
        >>> a.update_task(1, temp)
        True
        >>> a.update_task(144, temp)
        False
        >>> a.update_task_info(-1, "tEsT", "-.-", "2018", 3600)
        False
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
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit4.json")
        >>> temp = open(test_suits_folder_path + "/test_suit4.json", 'r').read()
        >>> a.delete_task(2)
        False
        >>> a.delete_task(1)
        True
        >>> file = open(test_suits_folder_path + "/test_suit4.json", "w")
        >>> file.write(temp)
        281
        >>> file.close()
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
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit5.json")
        >>> task = Task(1, "quest", "desc", parser.parse("2018"), parser.parse("2019"), False)
        >>> a.add_task(task) == task
        True
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
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit5.json")
        >>> task = Task(1, "quest", "desc", parser.parse("2018"), parser.parse("2018-06-03T00:00:34"), False)
        >>> b = a.create_task("quest", "desc", "2018", 34)
        >>> task.task_id = a.next_id - 1
        >>> b == task
        True
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
        >>> print(DataManager.__paginate_array__([1,2,3,4,5]))
        [1, 2, 3, 4, 5]
        >>> print(DataManager.__paginate_array__([1,2,3,4,5], offset=2))
        [3, 4, 5]
        >>> print(DataManager.__paginate_array__([1,2,3,4,5], offset=1, limit=3))
        [2, 3, 4]
        >>> print(DataManager.__paginate_array__([1,2,3,4,5], offset=-5, limit=0))
        [1, 2, 3, 4, 5]
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
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit1.json")
        >>> DataManager.__search_filter__(a.tasks).__len__()
        1
        >>> DataManager.__search_filter__(a.tasks, query="Just").__len__()
        0
        >>> DataManager.__search_filter__(a.tasks, query="Name").__len__()
        1
        >>> DataManager.__search_filter__(a.tasks, query="nam").__len__()
        1
        """
        if not isinstance(query, str) or query.__len__() == 0:
            return array
        return list(filter(lambda x: re.search(query, x.name + x.description, re.IGNORECASE), array))

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
        >>> a = DataManager.load_from_file(test_suits_folder_path + "/test_suit1.json")
        >>> DataManager.__paginate_and_search__(a.tasks).tasks.__len__()
        1
        >>> DataManager.__paginate_and_search__(a.tasks, offset=3).tasks.__len__()
        0
        >>> DataManager.__paginate_and_search__(a.tasks, query="nothing").tasks.__len__()
        1
        """
        filtered = DataManager.__search_filter__(array, query)
        length = filtered.__len__()
        tasks_result = DataManager.__paginate_array__(filtered, offset, limit)
        return Response(tasks_result, offset, limit, query, length, status_filter)
