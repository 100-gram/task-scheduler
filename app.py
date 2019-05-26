from flask import Flask, make_response, jsonify, session
from model.task import Task
from controller.datamanager import DataManager
import threading
import time
from console.interface import ConsoleInterface
from router.api import api


def test():
    print("")
    # task = Task(1, 'name1', 'description1', "Aug 28 1999 12:00AM", "Aug 30 1999 12:00AM", False)
    # task3 = Task(2, 'name2', 'description2', "Aug 28 1999 12:00AM", "Aug 30 1999 12:00AM", False)
    # task2 = Task(3, 'name3', 'description3', "Aug 28 1999 12:00AM", "Aug 30 1999 12:00AM", False)
    # task4 = Task.create(4, 'name4', 'ebgkerngk', "Aug 28 1999 12:00AM", 35)
    # task5 = Task.create(5, 'name5', 'ebgkerngk', "Aug 28 1999 12:00AM", 35)
    # task6 = Task.create(6, 'name6', 'ebgkerngk', "Aug 28 1999 12:00AM", 35)
    # dic = [task, task2, task3, task4, task5, task6]
    # dic.__len__()
    # for val in dic:
    #     DataManager.create_task('name4', 'ebgkerngk', "Aug 28 1999 12:00AM", 35)
    #
    # dict_new = DataManager.get_all()
    # for val in dict_new:
    #     print(val.name + val.description)
    #
    # print("\n\n")
    # t = 0
    # while t < 5:
    #     DataManager.update_task_info(dict_new[t].task_id, 'Edit taskVersion2', 'Edit Version2', "Aug 28 1999 12:00AM",
    #                                  55)
    #     t += 1
    # dict_new2 = DataManager.get_all()
    # DataManager.update_task(157, Task.create(4, 'Edit task', 'Edit', "Aug 28 1999 12:00AM", 55))
    # for val in dict_new2:
    #     print(val.name + val.description)


class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)
        self._activate_background_job()

    @staticmethod
    def _activate_background_job():
        test()

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
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run()
