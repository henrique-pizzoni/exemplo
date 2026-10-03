from pydantic import BaseModel


class TaskCreate(BaseModel):
    """O que o cliente envia no POST: so o titulo."""

    title: str


class Task(BaseModel):
    """Uma tarefa ja guardada."""

    title: str
    is_done: bool = False
