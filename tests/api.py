import pytest
import requests
from collections import namedtuple
import json

headers = {'content-type': 'application/json'}


def test_server_started():
    r = requests.get('http://127.0.0.1:5000/')
    assert r.status_code == 200


def test_get_all_tasks():
    r = requests.get('http://127.0.0.1:5000/api/v1/tasks')
    assert r.status_code == 200

    assert "application/json" in r.headers['Content-Type']
    assert "tasks" in r.json()


@pytest.fixture(scope="module")
def create_task():
    task = {"name": "TestVal", "description": "here", "date_start": "2019-05-12", "duration": 3600}
    r = requests.post('http://127.0.0.1:5000/api/v1/tasks',
                      data=json.dumps(task),
                      headers=headers)
    assert r.status_code == 201
    return json.loads(r.content, object_hook=lambda d: namedtuple('X', d.keys())(*d.values())).task


def test_put_task(create_task):
    task = {"name": "TestVal", "description": "there", "date_start": "2019-05-12", "duration": 3600}
    r = requests.put('http://127.0.0.1:5000/api/v1/tasks/{0}'.format(create_task.id),
                     data=json.dumps(task),
                     headers=headers)
    assert r.status_code == 200
    description = json.loads(r.content, object_hook=lambda d: namedtuple('X', d.keys())(*d.values())).task.description
    assert description == "there"


def test_unsuccessful_put_task(create_task):
    task = {"name": "TestVal", "description": "there", "date_start": "2019-05-12", "duration": 3600}
    r = requests.put('http://127.0.0.1:5000/api/v1/tasks/{0}'.format(create_task.id + 10),
                     data=json.dumps(task),
                     headers=headers)
    assert r.status_code == 404


def test_patch_task(create_task):
    query = {"set_uncompleted": False}
    r = requests.patch('http://127.0.0.1:5000/api/v1/tasks/complete/{0}'.format(create_task.id),
                       data=json.dumps(query),
                       headers=headers)
    assert r.status_code == 200
    task = json.loads(r.content, object_hook=lambda d: namedtuple('X', d.keys())(*d.values())).task
    task_is_completed = task.is_completed
    assert task_is_completed == True


def test_unsuccessful_patch_task(create_task):
    query = {"set_uncompleted": False}
    r = requests.patch('http://127.0.0.1:5000/api/v1/tasks/complete/{0}'.format(create_task.id + 10),
                       data=json.dumps(query),
                       headers=headers)
    assert r.status_code == 404


def test_delete_task(create_task):
    r = requests.delete('http://127.0.0.1:5000/api/v1/tasks/{0}'.format(create_task.id))
    assert r.status_code == 204


def test_unsuccessful_delete_task(create_task):
    r = requests.delete('http://127.0.0.1:5000/api/v1/tasks/asdf')
    assert r.status_code == 404
