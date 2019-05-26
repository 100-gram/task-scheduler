from model.task import Task


class Response:
    def __init__(self, tasks: [Task], offset: int, limit: int, query: str):
        self.tasks = tasks
        if isinstance(offset, int) and offset >= 0:
            self.offset = offset
        else:
            self.offset = 0
        if isinstance(limit, int) and limit > 0:
            self.limit = limit
        else:
            self.limit = None
        if isinstance(query, str) and str.__len__() > 0:
            self.query = query
        else:
            self.query = None
