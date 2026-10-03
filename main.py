from fastapi import FastAPI

from app.routes.task_routes import router as task_router

app = FastAPI(title="Exemplo C14")

app.include_router(task_router)
