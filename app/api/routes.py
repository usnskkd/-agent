from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.automation import AutomationCreate, AutomationRead
from app.schemas.execution import ExecutionRead
from app.schemas.task import TaskCreate, TaskRead
from app.services.automation_service import automation_service
from app.services.execution_service import execution_service
from app.services.task_service import task_service

templates = Jinja2Templates(directory="app/templates")

page_router = APIRouter()
api_router = APIRouter()


@page_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@api_router.get("/health")
def health():
    return {"status": "ok"}


@api_router.get("/tasks", response_model=list[TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return task_service.list_tasks(db)


@api_router.post("/tasks", response_model=TaskRead)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, payload)


@api_router.post("/tasks/{task_id}/run", response_model=ExecutionRead)
def run_task(task_id: int, db: Session = Depends(get_db)):
    execution = execution_service.run_task(db, task_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Task not found")
    return execution


@api_router.get("/executions", response_model=list[ExecutionRead])
def list_executions(db: Session = Depends(get_db)):
    return execution_service.list_executions(db)


@api_router.get("/executions/{execution_id}", response_model=ExecutionRead)
def get_execution(execution_id: int, db: Session = Depends(get_db)):
    execution = execution_service.get_execution(db, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return execution


@api_router.get("/automations", response_model=list[AutomationRead])
def list_automations(db: Session = Depends(get_db)):
    return automation_service.list_automations(db)


@api_router.post("/automations", response_model=AutomationRead)
def create_automation(payload: AutomationCreate, db: Session = Depends(get_db)):
    try:
        automation = automation_service.create_automation(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    automation_service.sync_jobs(db)
    return automation
