"""Funcoes puras: so recebem dados e devolvem dados.

Como nao dependem de nada externo, sao testadas sem mock.
"""

from app.models import Task


def count_done(tasks: list[Task]) -> int:
    return len([task for task in tasks if task.is_done])


def count_pending(tasks: list[Task]) -> int:
    return len(tasks) - count_done(tasks)


def completion_percentage(tasks: list[Task]) -> float:
    if not tasks:
        return 0.0
    return round(count_done(tasks) / len(tasks) * 100, 2)
