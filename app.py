from flask import Flask, make_response, jsonify, session
from model.task import Task
from controller.datamanager import DataManager
import threading
import time
from view.interface import ConsoleInterface
from router.api import api


class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)
        self._activate_background_job()

    @staticmethod
    def _activate_background_job():
        """
        asdfadf
        :return:
        """
        def run_job():
            time.sleep(3)
            ConsoleInterface.console_init()

        t1 = threading.Thread(target=run_job)
        t1.start()


app = FlaskApp(__name__)


app.register_blueprint(api, url_prefix='/api/v1')
app.config['data_manager'] = DataManager.load_from_file()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': error}), 404)


if __name__ == '__main__':
    app.run()
