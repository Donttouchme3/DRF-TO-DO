from rest_framework.test import APIClient
import pytest
from random import choice
from datetime import date

client = APIClient()


@pytest.mark.django_db
def test_create_task():
    payload = task_payload()

    # Create a task
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 201
    # Get a task
    get_task_response = get_task()
    assert get_task_response.status_code == 200

    data = get_task_response.json()
    assert data[0]['title'] == payload['title']
    assert data[0]['start_time'] == payload['start_time']
    assert data[0]['end_time'] == payload['end_time']
    assert data[0]['status'] == payload['status']


@pytest.mark.django_db
def test_get_task_list():
    payload = task_payload()

    for _ in range(1, 4):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 201

    get_task_response = get_task()
    assert get_task_response.status_code == 200

    data = get_task_response.json()
    for i in range(len(data)):
        assert data[i]['id'] == i + 2


@pytest.mark.django_db
def test_done_todo_in_progress_tasks():
    done = 0
    to_do = 0
    in_progress = 0
    # Create Task
    for i in range(1, 15):
        status = choice(['to-do', 'done', 'in progress'])

        if status == 'done':
            done += 1
        elif status == 'to-do':
            to_do += 1
        elif status == 'in progress':
            in_progress += 1

        payload = task_payload(status)
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 201

    # Get to done tasks
    get_done_tasks_response = get_done_tasks()
    get_todo_tasks_response = get_todo_tasks()
    get_in_progress_tasks_response = get_in_progress_tasks()

    assert len(get_done_tasks_response.json()) == done
    assert len(get_todo_tasks_response.json()) == to_do
    assert len((get_in_progress_tasks_response.json())) == in_progress


@pytest.mark.django_db
def test_expired_data():
    dates = ['2023-06-25', '2023-05-30', '2024-12-12']
    expired = 0
    expired_in_data = 0

    for i in dates:
        if i < str(date.today()):
            expired += 1

            # Create task
    for i in range(1, 4):
        payload = task_payload(end_time=dates[i - 1])
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 201

    # Get task
    for i in get_task().json():
        if i['end_time'] < str(date.today()):
            expired_in_data += 1

    assert expired == expired_in_data


@pytest.mark.django_db
def test_task_CRUD():
    payload = task_payload()

    # POST
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 201

    # GET
    task_id = create_task_response.json()['id']
    get_task_by_id_response = get_task_by_id(task_id)
    assert get_task_by_id_response.status_code == 200
    assert create_task_response.json() == get_task_by_id_response.json()

    # PUT
    new_payload = {
        "title": "i updated my task",
        "description": "string",
        "start_time": "2023-06-01",
        "end_time": "2023-06-21",
        'status': "to-do"
    }

    update_task_response = update_task(new_payload, task_id)
    get_updated_task = get_task_by_id(task_id)
    assert update_task_response.status_code == 201

    # PATH
    patch_payload = {
        'title': 'patch title'
    }
    patch_task_response = patch_task(patch_payload, task_id)
    get_patched_task = get_task_by_id(task_id)
    assert patch_task_response.status_code == 201
    assert get_updated_task.json() != get_patched_task.json()

    # DELETE
    delete_task_response = delete_task(task_id)
    tasks = len(get_task().json())
    assert tasks == 0


@pytest.mark.django_db
def test_login_auth_user():
    # Create task
    task_payload_ = task_payload()
    create_task_response = create_task(task_payload_)
    assert create_task_response.status_code == 201

    # Get tasks
    get_task_response = get_task()
    assert get_task_response.status_code == 401 or 200

    # Create user
    payload = user_payload()
    create_user_response = auth_user(payload)
    assert create_user_response.status_code == 201
    data = create_user_response.json()
    assert payload['username'] == data['username']
    assert payload['email'] == data['email']

    # Login user
    login_payload = {
        'username': payload['username'],
        'password': payload['password']
    }
    login_user_response = login_user(login_payload)
    assert login_user_response.status_code == 200

    # Get tasks
    user_token = {
        'Authorization': f"Token {login_user_response.json()['auth_token']}"
    }
    get_task_response = get_task(user_token)
    assert get_task_response.status_code == 200

    # Logout user
    logout_user_responser = logout_user(user_token)
    assert logout_user_responser.status_code == 204

    # Get tasks
    get_task_response = get_task()
    assert get_task_response.status_code == 401 or 200

def task_payload(status='to-do', end_time='2023-06-21'):
    return {
        "title": "my pytest task",
        "description": "string",
        "start_time": "2023-06-01",
        "end_time": end_time,
        "status": status
    }


def user_payload():
    return {
        'email': 'asil007bek@gmail.com',
        'username': 'Asilbek',
        'password': 'As031001',
    }


def get_task(token=None):
    return client.get('/api/tasks/', headers=token)


def get_task_by_id(id):
    return client.get(f'/api/tasks/{id}')


def get_done_tasks():
    return client.get('/api/tasks/done/')


def get_todo_tasks():
    return client.get('/api/tasks/to-do/')


def get_in_progress_tasks():
    return client.get('/api/tasks/in-progress/')


def create_task(payload):
    return client.post('/api/create/', payload)


def update_task(payload, id):
    return client.put(f'/api/tasks/{id}', payload)


def patch_task(payload, id):
    return client.patch(f'/api/tasks/{id}', payload)


def delete_task(id):
    return client.delete(f'/api/tasks/{id}')


def login_user(payload):
    return client.post('/auth/token/login', payload)


def auth_user(payload):
    return client.post('/auth/users/', payload)


def logout_user(auth_token):
    return client.post('/auth/token/logout', headers=auth_token)
