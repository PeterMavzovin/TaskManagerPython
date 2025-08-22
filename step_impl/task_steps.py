import json
import uuid
import httpx

from getgauge.python import step, before_scenario, after_scenario, data_store

BASE_URL = "http://127.0.0.1:8000"
client = None

@before_scenario
def setup_client():
    global client
    client = httpx.Client(base_url=BASE_URL)
    data_store.scenario["client"] = client

@after_scenario
def teardown_client():
    if client:
        client.close()

@step("Создать задачу с названием <title> и описанием <description>")
def create_task_with_title_and_description(title, description):
    payload = {"title": title, "description": description}
    response = data_store.scenario["client"].post("/tasks/", json=payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    task_data = response.json()
    assert task_data["title"] == title
    assert task_data["description"] == description
    assert "id" in task_data
    data_store.scenario["current_task_id"] = task_data["id"]
    data_store.scenario["created_task"] = task_data

@step("Получить список задач")
def get_list_of_tasks():
    response = data_store.scenario["client"].get("/tasks/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data_store.scenario["tasks_list"] = response.json()

@step("Список задач должен содержать задачу с названием <title>")
def task_list_should_contain_task_with_title(title):
    found = False
    for task in data_store.scenario["tasks_list"]:
        if task["title"] == title:
            found = True
            break
    assert found, f"Task with title '{title}' not found in the list."

@step("Получить задачу по ID")
def get_task_by_id():
    task_id = data_store.scenario["current_task_id"]
    response = data_store.scenario["client"].get(f"/tasks/{task_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data_store.scenario["retrieved_task"] = response.json()

@step("Полученная задача должна иметь название <title> и описание <description>")
def retrieved_task_should_have_title_and_description(title, description):
    task = data_store.scenario["retrieved_task"]
    assert task["title"] == title
    assert task["description"] == description

@step("Обновить задачу: название <new_title>, описание <new_description>, статус <new_status>")
def update_task(new_title, new_description, new_status):
    task_id = data_store.scenario["current_task_id"]
    payload = {}
    if new_title != "None":
        payload["title"] = new_title
    if new_description != "None":
        payload["description"] = new_description
    if new_status != "None":
        payload["status"] = new_status

    response = data_store.scenario["client"].put(f"/tasks/{task_id}", json=payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    updated_task_data = response.json()
    
    if new_title != "None":
        assert updated_task_data["title"] == new_title
    if new_description != "None":
        assert updated_task_data["description"] == new_description
    if new_status != "None":
        assert updated_task_data["status"] == new_status
    data_store.scenario["updated_task"] = updated_task_data


@step("Удалить задачу")
def delete_task():
    task_id = data_store.scenario["current_task_id"]
    response = data_store.scenario["client"].delete(f"/tasks/{task_id}")
    assert response.status_code == 204, f"Expected 204, got {response.status_code}: {response.text}"

@step("Попытаться получить удаленную задачу")
def try_to_get_deleted_task():
    task_id = data_store.scenario["current_task_id"]
    response = data_store.scenario["client"].get(f"/tasks/{task_id}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.text}"
    
@step("Создать несколько задач:")
def create_multiple_tasks(table):
    for row in table.rows:
        title = row["title"]
        description = row["description"]
        payload = {"title": title, "description": description}
        response = data_store.scenario["client"].post("/tasks/", json=payload)
        assert response.status_code == 200, f"Failed to create task: {title}"
        
@step("Получить список задач со статусом <status>")
def get_list_of_tasks_by_status(status):
    response = data_store.scenario["client"].get(f"/tasks/?status={status}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data_store.scenario["tasks_list_by_status"] = response.json()

@step("Список задач со статусом <status> должен содержать <count> задач")
def tasks_with_status_should_have_count(status, count):
    tasks = data_store.scenario["tasks_list_by_status"]
    assert len(tasks) == int(count), f"Expected {count} tasks with status {status}, but got {len(tasks)}"
    for task in tasks:
        assert task["status"] == status, f"Task {task['id']} has wrong status {task['status']}, expected {status}"