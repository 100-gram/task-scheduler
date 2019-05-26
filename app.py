from flask import make_response, jsonify
from controller.datamanager import DataManager
from werkzeug.exceptions import HTTPException
from app.server import Server
from router.api import api
import logging


app = Server(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

app.register_blueprint(api, url_prefix='/api/v1')
app.config['data_manager'] = DataManager.load_from_file()


@app.route('/')
def hello_world():
    return 'Api could be found at <a href="/api/v1">/api/v1</a>'


@app.errorhandler(HTTPException)
def error_handler(error):
    return make_response(jsonify({'error': error.description}), error.code)


if __name__ == '__main__':
    app.run()
