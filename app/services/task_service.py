from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate


class TaskService:
    def list_tasks(self, db: Session) -> list[Task]:
        return db.query(Task).order_by(Task.id.desc()).all()

    def create_task(self, db: Session, payload: TaskCreate) -> Task:
        task = Task(
            name=payload.name,
            goal=payload.goal,
            channel=payload.channel,
            audience=payload.audience,
            budget=payload.budget,
            metadata_json=payload.metadata,
            status="ready",
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task


task_service = TaskService()
