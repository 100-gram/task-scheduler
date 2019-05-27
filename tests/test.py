from router.api import api
from flask import request, Flask
from controller.datamanager import DataManager
import requests


def setup():
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/api/v1')
    app.config['data_manager'] = DataManager.load_from_file()
    app.run()


def teardown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def test_upper():
    r = requests.delete('http://0.0.0.0.0/api/v1/tasks/1488')
    assert r.status_code == 404
    teardown()
