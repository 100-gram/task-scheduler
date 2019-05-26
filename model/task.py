from dateutil import parser
from datetime import timedelta, datetime


class Task:
    def __init__(self, task_id: int, name: str, description: str, date_start: datetime, date_end: datetime,
                 is_completed: bool):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.date_start = date_start
        self.date_end = date_end
        self.is_completed = is_completed

    def __json__(self):
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
        return cls(json_obj['id'], json_obj['name'], json_obj['description'], parser.parse(json_obj['date_start']),
                   parser.parse(json_obj['date_end']), json_obj['is_completed'])

    @classmethod
    def create(cls, task_id: int, name: str, description: str, date_start: str, duration: int):
        return cls(task_id, name, description, parser.parse(date_start),
                   parser.parse(date_start) + timedelta(seconds=duration), False)

    def completed(self):
        return self.is_completed

    def is_finished(self):
        return datetime.now() > self.date_end

    def is_running(self):
        return self.date_start < datetime.now() < self.date_end

    def make_completed(self):
        self.is_completed = True

    def make_uncompleated(self):
        self.is_completed = False
