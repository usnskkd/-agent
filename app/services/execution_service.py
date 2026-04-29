from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.orchestrator import orchestrator
from app.models.execution import Execution
from app.models.task import Task


class ExecutionService:
    def list_executions(self, db: Session) -> list[Execution]:
        return db.query(Execution).order_by(Execution.id.desc()).all()

    def get_execution(self, db: Session, execution_id: int) -> Execution | None:
        return db.query(Execution).filter(Execution.id == execution_id).first()

    def run_task(self, db: Session, task_id: int) -> Execution | None:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None

        task_payload = {
            "goal": task.goal,
            "channel": task.channel,
            "audience": task.audience,
            "budget": task.budget,
            "metadata": task.metadata_json,
        }
        result = orchestrator.run(task_payload)
        execution = Execution(task_id=task.id, status="success", result_json=result)
        db.add(execution)
        db.commit()
        db.refresh(execution)
        return execution


execution_service = ExecutionService()
