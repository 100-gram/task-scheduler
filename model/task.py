from dateutil import parser
from datetime import timedelta, datetime
from config.config import test_suits_folder_path
import simplejson

"""
Class that describe Task

Provide all methods to manage Task 
"""


class Task:
    def __init__(self, task_id: int, name: str, description: str, date_start: datetime, date_end: datetime,
                 is_completed: bool):
        """
        Constructor for Task object

        :param task_id: id of Task
        :param name: name of Task
        :param description: description of Task
        :param date_start: start date of Task
        :param date_end: end date of Task
        :param is_completed: status of Task
        """
        self.task_id = task_id
        self.name = name
        self.description = description
        self.date_start = date_start
        self.date_end = date_end
        self.is_completed = is_completed

    def __eq__(self, other):
        """
        Compare two Task entity

        :param other: second Task entity
        :return: True if entity is equal else False
        >>> a = Task(1, "name1", "descr1", datetime(2012, 2, 2, 2, 2, 2), datetime(2013, 3, 3, 3, 3, 3), True)
        >>> b = Task(1, "name1", "descr1", datetime(2012, 2, 2, 2, 2, 2), datetime(2013, 3, 3, 3, 3, 3), True)
        >>> c = Task(2, "name2", "descr2", datetime(2012, 2, 2, 2, 2, 2), datetime(2013, 3, 3, 3, 3, 3), True)
        >>> a.__eq__(b)
        True
        >>> a.__eq__(c)
        False
        """
        if not isinstance(other, Task):
            return False
        return self.task_id == other.task_id and self.name == other.name and self.description == other.description \
            and self.date_start == other.date_start and self.date_end == other.date_end\
            and self.is_completed == other.is_completed

    def __json__(self):
        """
        JSON serialization for DataManager object

        :return: dict with all inner fields
        >>> a = Task(1, "name1", "descr1", datetime(2012, 2, 2, 2, 2, 2), datetime(2013, 3, 3, 3, 3, 3), True)
        >>> a.__json__().__str__() == open(test_suits_folder_path + "/test_task.txt", 'r').read()
        True
        """
        return {
            'id': self.task_id,
            'name': self.name,
            'description': self.description,
            'date_start': self.date_start.isoformat(),
            'date_end': self.date_end.isoformat(),
            'is_completed': self.is_completed
        }

    for_json = __json__  # supported by simplejson

    @classmethod
    def from_json(cls, json_obj):
        """
        Creating Task object from JSON object

        :param json_obj: JSON object (dict)
        :return: instance of Task
        >>> a = Task(1, "name1", "descr1", datetime(2012, 2, 2, 2, 2, 2), datetime(2013, 3, 3, 3, 3, 3), True)
        >>> data_str = open(test_suits_folder_path + "/test_task.json", 'r').read()
        >>> storage_obj = simplejson.loads(data_str)
        >>> b = Task.from_json(storage_obj)
        >>> a.__eq__(b)
        True
        """
        return cls(json_obj['id'], json_obj['name'], json_obj['description'], parser.parse(json_obj['date_start']),
                   parser.parse(json_obj['date_end']), json_obj['is_completed'])

    @classmethod
    def create(cls, task_id: int, name: str, description: str, date_start: str, duration: int):
        """
        Create new Task

        :param task_id:  id of new Task
        :param name: name of new Task
        :param description: description of new Task
        :param date_start: start date of new Task
        :param duration: duration of new Task
        :return: created Task entity
        >>> a = Task(1, "name1", "descr1", datetime(2012, 2, 2, 2, 2, 2), datetime(2012, 2, 2, 2, 2, 12), False)
        >>> b = Task.create(1, "name1", "descr1", "2012-02-02 02:02:02", 10)
        >>> a.__eq__(b)
        True
        """
        return cls(task_id, name, description, parser.parse(date_start),
                   parser.parse(date_start) + timedelta(seconds=duration), False)

    def completed(self):
        """
        Get status of Task

        :return: status of Task
        >>> a = Task(1, "name1", "descr1", datetime(2012, 2, 2, 2, 2, 2), datetime(2012, 2, 2, 2, 12, 2), False)
        >>> a.completed()
        False
        """
        return self.is_completed

    def is_finished(self):
        """
        Get finished status of Task

        :return: True if Task is finished else False
        >>> a = Task(1, "name1", "descr1", datetime(2012, 2, 2, 2, 2, 2), datetime(2012, 2, 2, 2, 12, 2), False)
        >>> a.is_finished()
        True
        """
        return datetime.now() > self.date_end

    def is_running(self):
        """
        Get running status of Task

        :return: True if Task is running else False
        >>> a = Task(1, "name1", "descr1", datetime(2012, 2, 2, 2, 2, 2), datetime(2012, 2, 2, 2, 12, 2), False)
        >>> a.is_running()
        False
        """
        return self.date_start < datetime.now() < self.date_end

    def make_completed(self):
        """
        Complete Task

        :return: None
        >>> a = Task(1, "name1", "descr1", datetime(2012, 2, 2, 2, 2, 2), datetime(2012, 2, 2, 2, 12, 2), False)
        >>> a.make_completed()
        >>> a.is_completed = True
        """
        self.is_completed = True

    def make_uncompleted(self):
        """
        Incomplete Task

        :return:
        >>> a = Task(1, "name1", "descr1", datetime(2012, 2, 2, 2, 2, 2), datetime(2012, 2, 2, 2, 12, 2), True)
        >>> a.make_uncompleted()
        >>> a.is_completed = False
        """
        self.is_completed = False
