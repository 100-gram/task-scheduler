from enum import Enum, auto

"""
Enum of Task status

Represents all possible statuses of task
"""


class TaskStatus(Enum):
    COMPLETED = auto()
    UNCOMPLETED = auto()
    PLANNED = auto()
    RUNNING = auto()
    FINISHED = auto()

    def __json__(self):
        """
        JSON serialization for TaskStatus

        :return: Task status name
        """
        return self.name

    for_json = __json__  # supported by simplejson
