from flask import make_response, jsonify
from controller.datamanager import DataManager
from werkzeug.exceptions import HTTPException
from flask_restful import Api
from server.server import Server
from router.api import api
from router.task_list import TaskList
from router.task import Task
import logging

app = Server(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True
api_ = Api(app)
api_.add_resource(TaskList, '/api/v2/tasks')
api_.add_resource(Task, '/api/v2/tasks/<int:task_id>')
app.register_blueprint(api, url_prefix='/api/v1')
app.config['data_manager'] = DataManager.load_from_file()


@app.route('/')
def hello_world():
    return 'Api could be found at <a href="/api/v1">/api/v1</a>'


@app.errorhandler(HTTPException)
def error_handler(error):
    return make_response(jsonify({'error': error.description}), error.code)


if __name__ == '__main__':
    app.run(debug=True)
