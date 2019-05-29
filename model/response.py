from model.task import Task

"""
Wrapper for pagination Response

Provide all methods to manage Response
"""

class Response:
    def __init__(self, tasks: [Task], offset: int, limit: int, query: str, count_all: int, status_filter=None):
        """
        Constructor for Response object

        :param tasks: list of Tasks
        :param offset: count of skipping tasks
        :param limit: count of Tasks in page
        :param query: searched parameter
        :param count_all: count of all Tasks
        :param status_filter: searched Task status
        """
        self.tasks = tasks
        self.count_all = count_all
        self.status_filter = status_filter
        self.offset = offset if isinstance(offset, int) and offset >= 0 else 0
        self.limit = limit if isinstance(limit, int) and limit > 0 else None
        self.query = query if isinstance(query, str) and query.__len__() > 0 else None

    def __json__(self):
        """
        JSON serialization for DataManager object

        :return: dict with all inner fields
        """
        return {
            'tasks': self.tasks,
            'offset': self.offset,
            'limit': self.limit,
            'query': self.query,
            'count_all': self.count_all,
            'status_filter': self.status_filter
        }

    for_json = __json__  # supported by simplejson
