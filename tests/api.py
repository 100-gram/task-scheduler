from model.task import Task
import requests


def test_server_started():
    r = requests.get('http://127.0.0.1:5000/')
    assert r.status_code == 200


def test_get_all_tasks():
    r = requests.get('http://127.0.0.1:5000/api/v1/tasks')
    assert r.status_code == 200

    assert "application/json" in r.headers['Content-Type']
    assert "tasks" in r.json()


def test_create_task():
    task = Task.create(task_id=0, name="TestVal", description="here", date_start="2019-05-12", duration=3600)
    r = requests.post('http://127.0.0.1:5000/api/v1/tasks', json=task.__json__())
    print(task.__json__())
    assert r.status_code == 201
    assert r.json()
