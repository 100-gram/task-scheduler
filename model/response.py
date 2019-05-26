from model.task import Task


class Response:
    def __init__(self, tasks: [Task], offset: int, limit: int, query: str, count_all: int, status):
        self.tasks = tasks
        self.count_all = count_all
        self.status = status
        if isinstance(offset, int) and offset >= 0:
            self.offset = offset
        else:
            self.offset = 0
        if isinstance(limit, int) and limit > 0:
            self.limit = limit
        else:
            self.limit = None
        if isinstance(query, str) and query.__len__() > 0:
            self.query = query
        else:
            self.query = None

    def __json__(self):
        return {
            'tasks': self.tasks,
            'offset': self.offset,
            'limit': self.limit,
            'query': self.query,
            'count_all': self.count_all,
            'status': self.status
        }

    for_json = __json__  # supported by simplejson
