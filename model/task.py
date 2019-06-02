from dateutil import parser
from datetime import timedelta, datetime

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
        """
        return cls(task_id, name, description, parser.parse(date_start),
                   parser.parse(date_start) + timedelta(seconds=duration), False)

    def completed(self):
        """
        Get status of Task

        :return: status of Task
        """
        return self.is_completed

    def is_finished(self):
        """
        Get finished status of Task

        :return: True if Task is finished else False
        """
        return datetime.now() > self.date_end

    def is_running(self):
        """
        Get running status of Task

        :return: True if Task is running else False
        """
        return self.date_start < datetime.now() < self.date_end

    def make_completed(self):
        """
        Complete Task

        :return: None
        """
        self.is_completed = True

    def make_uncompleted(self):
        """
        Incomplete Task

        :return: None
        """
        self.is_completed = False
