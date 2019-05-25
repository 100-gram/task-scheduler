from dateutil import parser
from datetime import timedelta


class Task:
    def __init__(self, id, name, description, date_start, date_end, is_complited):
        self.name = name
        self.description = description
        self.date_start = date_start
        self.date_end = date_end
        self.is_complited = is_complited

    def __json__(self):
        return {
            'name': self.name,
            'description': self.description,
            'date_start': str(self.date_start),
            'date_end': str(self.date_end),
            'is_complited': self.is_complited
        }

    for_json = __json__  # supported by simplejson

    @classmethod
    def from_json(cls, json_obj):
        obj = cls(json_obj['name'], json_obj['description'], parser.parse(json_obj['date_start']),
                  parser.parse(json_obj['date_end']),
                  json_obj['is_complited'])
        return obj

    @classmethod
    def create(cls, name, description, date_start, duration):
        return cls(name, description, parser.parse(date_start), parser.parse(date_start) + timedelta(minutes=duration),
                   False)
