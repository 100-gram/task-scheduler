from flask import Flask, make_response, jsonify, request
from model.task import Task
from os import path
import json
import simplejson

app = Flask(__name__)

storage_path = path.dirname(path.realpath(__file__)) + '\\data\\tasks.json'

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


incomes = [
  {'description': 'salary', 'amount': 5000}
]


@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204


if __name__ == '__main__':
    task = Task('name1', 'description1', "Aug 28 1999 12:00AM", "Aug 30 1999 12:00AM", False)
    task3 = Task('name2', 'description2', "Aug 28 1999 12:00AM", "Aug 30 1999 12:00AM", False)
    task2 = Task('name3', 'description3', "Aug 28 1999 12:00AM", "Aug 30 1999 12:00AM", False)
    task4 = Task.create('name4', 'ebgkerngk', "Aug 28 1999 12:00AM", 35)
    task5 = Task.create('name5', 'ebgkerngk', "Aug 28 1999 12:00AM", 35)
    task6 = Task.create('name6', 'ebgkerngk', "Aug 28 1999 12:00AM", 35)
    dic = [task, task2, task3, task4, task5, task6]
    with open(storage_path, 'w') as outfile:
        simplejson.dump(dic, outfile, indent=4, for_json=True)
    new_str = open(storage_path, 'r').read()
    print(new_str)
    obj2_dict = simplejson.loads(new_str)
    dict_new = []
    for val in obj2_dict:
        dict_new.append(Task.from_json(val))
    for val in dict_new:
        print(val.name + val.description)