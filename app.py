from flask import Flask, make_response, jsonify
from ConsoleInterface import console_init

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    console_init()
    app.run(debug=True)
