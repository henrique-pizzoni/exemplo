from fastapi import APIRouter, HTTPException

from app.models import Task, TaskCreate
from app.repositories.task_repository import JsonTaskRepository
from app.services import task_stats_service
from app.services.task_service import TaskNotFoundError, TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])

service = TaskService(JsonTaskRepository())


@router.post("")
def create_task(payload: TaskCreate) -> Task:
    try:
        return service.create_task(payload.title)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("")
def list_tasks(limit: int = 10) -> list[Task]:
    return service.list_tasks(limit)


@router.get("/stats")
def get_stats() -> dict:
    tasks = service.list_tasks()
    return {
        "done": task_stats_service.count_done(tasks),
        "pending": task_stats_service.count_pending(tasks),
        "completion_percentage": task_stats_service.completion_percentage(tasks),
    }


@router.get("/{task_id}")
def get_task(task_id: int) -> Task:
    try:
        return service.get_task(task_id)
    except TaskNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
