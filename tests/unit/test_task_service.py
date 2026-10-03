from unittest.mock import Mock

import pytest

from app.models import Task
from app.repositories.task_repository import JsonTaskRepository
from app.services.task_service import TaskNotFoundError, TaskService


class TestTaskService:
    def test_create_task_rejects_an_empty_title(self):
        # fixtures (sem mock: a validacao acontece antes do repositorio)
        service = TaskService(JsonTaskRepository(file_path="unused.json"))

        # processamento / assertivas
        with pytest.raises(ValueError):
            service.create_task("   ")

    def test_create_task_does_not_touch_the_json_file_when_title_is_empty(self):
        # fixtures
        repository = Mock(spec=JsonTaskRepository)
        service = TaskService(repository)

        # processamento
        with pytest.raises(ValueError):
            service.create_task("   ")

        # assertivas
        repository.add.assert_not_called()

    def test_create_task_saves_the_task_in_the_json_file(self):
        # fixtures
        repository = Mock(spec=JsonTaskRepository)
        repository.add.return_value = Task(title="Estudar", is_done=False)
        service = TaskService(repository)

        # processamento
        created_task = service.create_task("  Estudar  ")

        # assertivas
        repository.add.assert_called_once_with(Task(title="Estudar", is_done=False))
        assert created_task.title == "Es"

    def test_list_tasks_returns_only_the_requested_limit(self):
        # fixtures
        repository = Mock(spec=JsonTaskRepository)
        repository.read_all.return_value = [
            Task(title="Estudar", is_done=True),
            Task(title="Treinar", is_done=False),
            Task(title="Dormir", is_done=False),
        ]
        service = TaskService(repository)

        # processamento
        tasks = service.list_tasks(limit=2)

        # assertivas
        repository.read_all.assert_called_once()
        assert [task.title for task in tasks] == ["Estudar", "Treinar"]

    def test_get_task_raises_error_when_task_is_not_in_the_json_file(self):
        # fixtures
        repository = Mock(spec=JsonTaskRepository)
        repository.get_by_id.return_value = None
        service = TaskService(repository)

        # processamento
        with pytest.raises(TaskNotFoundError):
            service.get_task(99)

        # assertivas
        repository.get_by_id.assert_called_once_with(99)
