from flask import Blueprint, make_response, jsonify, abort, request
from model.datamanager import DataManager

api = Blueprint('api/v1/', __name__)


@api.route('/')
def index():
    return jsonify({'info': 'get info about api docs somewhere'})


@api.route('/tasks', methods=['GET'])
def get_tasks():
    DataManager.get_all()
    return jsonify({"tasks": DataManager.get_all()})


@api.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    item = list(filter(lambda t: t['id'] == task_id, DataManager.get_all()))
    if len(item) == 0:
        abort(404)
    return jsonify({'task': item[0]})


@api.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'name' not in request.json:
        abort(400)
        DataManager.create_task(request.json['name'])  # TODO

    return jsonify({'task': "here should be task"}), 201


@api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_item(task_id):
    DataManager.delete_task(task_id)
    return jsonify({'result': True})


@api.route('/tasks/<int:task_id>', methods=['PUT'])
def update_item(task_id):
    DataManager.update_task(task_id, ) # TODO
    return jsonify({'item': "here should de task"})

