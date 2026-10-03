import pytest

from app.models import Task
from app.services import task_stats_service


class TestTaskStatsService:
    def test_count_done_counts_only_finished_tasks(self):
        # fixtures
        tasks = [
            Task(title="Estudar", is_done=True),
            Task(title="Treinar", is_done=False),
            Task(title="Dormir", is_done=True),
        ]

        # processamento
        total = task_stats_service.count_done(tasks)

        # assertivas
        assert total == 2

    def test_count_pending_counts_only_unfinished_tasks(self):
        # fixtures
        tasks = [
            Task(title="Estudar", is_done=True),
            Task(title="Treinar", is_done=False),
            Task(title="Dormir", is_done=False),
        ]

        # processamento
        total = task_stats_service.count_pending(tasks)

        # assertivas
        assert total == 2

    def test_completion_percentage_returns_the_ratio_of_finished_tasks(self):
        # fixtures
        tasks = [
            Task(title="Estudar", is_done=True),
            Task(title="Treinar", is_done=False),
            Task(title="Dormir", is_done=False),
            Task(title="Ler", is_done=False),
        ]

        # processamento
        percentage = task_stats_service.completion_percentage(tasks)

        # assertivas
        assert percentage == 25.0

    def test_completion_percentage_returns_zero_for_an_empty_list(self):
        # fixtures
        tasks = []

        # processamento
        percentage = task_stats_service.completion_percentage(tasks)

        # assertivas
        assert percentage == 0.0

    def test_count_done_rejects_none_instead_of_a_list(self):
        # fixtures
        tasks = None

        # processamento + assertivas
        # pytest.raises faz as duas coisas: executa o bloco e so passa
        # se a excecao indicada for lancada dentro dele.
        with pytest.raises(TypeError):
            task_stats_service.count_done(tasks)
