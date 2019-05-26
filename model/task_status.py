from enum import Enum, auto


class TaskStatus(Enum):
    COMPLETED = auto()
    UNCOMPLETED = auto()
    PLANNED = auto()
    RUNNING = auto()
    FINISHED = auto()
