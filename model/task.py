from dateutil import parser
from datetime import timedelta


class Task:
    def __init__(self, task_id: int, name: str, description: int, date_start, date_end, is_complited: bool):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.date_start = date_start
        self.date_end = date_end
        self.is_complited = is_complited

    def __json__(self):
        return {
            'id': self.task_id,
            'name': self.name,
            'description': self.description,
            'date_start': str(self.date_start),
            'date_end': str(self.date_end),
            'is_complited': self.is_complited
        }

    for_json = __json__  # supported by simplejson

    @classmethod
    def from_json(cls, json_obj):
        obj = cls(json_obj['id'], json_obj['name'], json_obj['description'], parser.parse(json_obj['date_start']),
                  parser.parse(json_obj['date_end']),
                  json_obj['is_complited'])
        return obj

    @classmethod
    def create(cls, task_id: int, name: str, description: str, date_start, duration: int):
        return cls(task_id, name, description, parser.parse(date_start),
                   parser.parse(date_start) + timedelta(minutes=duration),
                   False)
