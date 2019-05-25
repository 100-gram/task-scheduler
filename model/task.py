from dateutil import parser


class Task:
    def __init__(self, name, description, date_start, duration):
        self.name = name
        self.description = description
        self.date_start = parser.parse(date_start)
        self.date_end = self.date_start + duration
        self.is_complited = False
