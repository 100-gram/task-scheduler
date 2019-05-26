from enum import Enum, auto


class TaskStatus(Enum):
    COMPLETED = auto()
    UNCOMPLETED = auto()
    PLANNED = auto()
    RUNNING = auto()
    FINISHED = auto()

    def __json__(self):
        return self.name

    for_json = __json__  # supported by simplejson
