from app.models import Task
from app.repositories.task_repository import JsonTaskRepository


class TaskNotFoundError(Exception):
    """Lancada quando a tarefa pedida nao existe."""


class TaskService:
    """Regras de negocio das tarefas.

    Recebe o repositorio pelo construtor (injecao de dependencia).
    E isso que permite trocar o repositorio por um mock no teste.
    """

    def __init__(self, repository: JsonTaskRepository):
        self.repository = repository

    def create_task(self, title: str) -> Task:
        clean_title = (title or "").strip()
        if not clean_title:
            raise ValueError("O titulo da tarefa nao pode ser vazio")
        return self.repository.add(Task(title=clean_title, is_done=False))

    def list_tasks(self, limit: int | None = None) -> list[Task]:
        tasks = self.repository.read_all()
        if limit is None:
            return tasks
        return tasks[:limit]

    def get_task(self, task_id: int) -> Task:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} Not Found")
        return task
