from flask import Flask, make_response, jsonify, request
from model.task import Task
from os import path
from model.datamanager import DataManager
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
    task = Task(1, 'name1', 'description1', "Aug 28 1999 12:00AM", "Aug 30 1999 12:00AM", False)
    task3 = Task(2, 'name2', 'description2', "Aug 28 1999 12:00AM", "Aug 30 1999 12:00AM", False)
    task2 = Task(3, 'name3', 'description3', "Aug 28 1999 12:00AM", "Aug 30 1999 12:00AM", False)
    task4 = Task.create(4, 'name4', 'ebgkerngk', "Aug 28 1999 12:00AM", 35)
    task5 = Task.create(5, 'name5', 'ebgkerngk', "Aug 28 1999 12:00AM", 35)
    task6 = Task.create(6, 'name6', 'ebgkerngk', "Aug 28 1999 12:00AM", 35)
    dic = [task, task2, task3, task4, task5, task6]
    for val in dic:
        DataManager.create_task('name4', 'ebgkerngk', "Aug 28 1999 12:00AM", 35)

    dict_new = DataManager.get_all()
    for val in dict_new:
        print(val.name + val.description)

    print("\n\n")
    t = 0
    while t < 5:
        DataManager.update_task_info(dict_new[t].task_id, 'Edit taskVersion2', 'Edit Version2', "Aug 28 1999 12:00AM",
                                     55, True)
        t += 1
    dict_new2 = DataManager.get_all()
    DataManager.update_task(157, Task.create(4, 'Edit task', 'Edit', "Aug 28 1999 12:00AM", 55))
    for val in dict_new2:
        print(val.name + val.description)