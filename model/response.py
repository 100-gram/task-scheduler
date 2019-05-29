from model.task import Task


class Response:
    def __init__(self, tasks: [Task], offset: int, limit: int, query: str, count_all: int, status_filter=None):
        self.tasks = tasks
        self.count_all = count_all
        self.status_filter = status_filter
        self.offset = offset if isinstance(offset, int) and offset >= 0 else 0
        self.limit = limit if isinstance(limit, int) and limit > 0 else None
        self.query = query if isinstance(query, str) and query.__len__() > 0 else None

    def __json__(self):
        return {
            'tasks': self.tasks,
            'offset': self.offset,
            'limit': self.limit,
            'query': self.query,
            'count_all': self.count_all,
            'status_filter': self.status_filter
        }

    for_json = __json__  # supported by simplejson
