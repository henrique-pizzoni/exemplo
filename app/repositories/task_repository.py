import json
from pathlib import Path

from app.models import Task


class JsonTaskRepository:
    """Guarda as tarefas em um arquivo JSON no disco.

    E a unica camada que encosta no disco. Por isso, nos testes
    unitarios do service, essa classe e trocada por um mock.

    """

    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = Path(file_path)

    def read_all(self) -> list[Task]:
        if not self.file_path.exists():
            return []
        with open(self.file_path, encoding="utf-8") as file:
            raw_tasks = json.load(file)
        return [Task(**raw_task) for raw_task in raw_tasks]

    def save_all(self, tasks: list[Task]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([task.model_dump() for task in tasks], file, indent=2)

    def add(self, task: Task) -> Task:
        tasks = self.read_all()
        tasks.append(task)
        self.save_all(tasks)
        return task

    def get_by_id(self, task_id: int) -> Task | None:
        tasks = self.read_all()
        if 0 <= task_id < len(tasks):
            return tasks[task_id]
        return None
