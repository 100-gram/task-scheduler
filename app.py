from flask import make_response, jsonify
from werkzeug.exceptions import HTTPException
from flask_restful import Api
from server.server import Server
from router.api import api
from router.task_list import TaskList
from router.task import Task
from config.config import disable_log, api_prefix

app = Server(__name__)
restful_api = Api(app)
restful_api.add_resource(TaskList, f'{api_prefix}/tasks')
restful_api.add_resource(Task, f'{api_prefix}/tasks/<int:task_id>')
app.register_blueprint(api, url_prefix=api_prefix)


@app.route('/')
def root_handler():
    return f'Api could be found at <a href="{api_prefix}">{api_prefix}</a>'


@app.errorhandler(HTTPException)
def error_handler(error):
    return make_response(jsonify({'error': error.description}), error.code)


if __name__ == '__main__':
    disable_log(app)
    app.run()
