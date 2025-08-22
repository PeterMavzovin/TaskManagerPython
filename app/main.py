from typing import Dict, List, Optional
import uuid

from fastapi import FastAPI, HTTPException

from app.models import Task, TaskCreate, TaskUpdate, TaskStatus

app = FastAPI()

# In-memory storage for tasks
tasks: Dict[uuid.UUID, Task] = {}

@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate):
    new_task = Task(title=task.title, description=task.description)
    tasks[new_task.id] = new_task
    return new_task

@app.get("/tasks/", response_model=List[Task])
async def get_tasks(status: Optional[TaskStatus] = None):
    if status:
        return [task for task in tasks.values() if task.status == status]
    return list(tasks.values())

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: uuid.UUID):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: uuid.UUID, task_update: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    existing_task = tasks[task_id]
    update_data = task_update.model_dump(exclude_unset=True)
    updated_task = existing_task.model_copy(update=update_data)
    tasks[task_id] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: uuid.UUID):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return ""