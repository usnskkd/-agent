from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.scheduler import scheduler_service
from app.db.base import SessionLocal
from app.models.automation import Automation
from app.models.task import Task
from app.schemas.automation import AutomationCreate
from app.services.execution_service import execution_service


class AutomationService:
    def list_automations(self, db: Session) -> list[Automation]:
        return db.query(Automation).order_by(Automation.id.desc()).all()

    def create_automation(self, db: Session, payload: AutomationCreate) -> Automation:
        task = db.query(Task).filter(Task.id == payload.task_id).first()
        if not task:
            raise ValueError("Task not found")

        automation = Automation(
            task_id=payload.task_id,
            name=payload.name,
            interval_minutes=payload.interval_minutes,
            enabled="true" if payload.enabled else "false",
        )
        db.add(automation)
        db.commit()
        db.refresh(automation)
        return automation

    def sync_jobs(self, db: Session):
        automations = db.query(Automation).all()
        valid_job_ids: set[str] = set()
        for automation in automations:
            if automation.enabled != "true":
                continue
            job_id = f"automation:{automation.id}"
            valid_job_ids.add(job_id)
            scheduler_service.add_or_replace_interval_job(
                job_id=job_id,
                func=self._run_automation,
                minutes=automation.interval_minutes,
                args=[automation.task_id],
            )
        scheduler_service.remove_missing_jobs(valid_job_ids)

    def _run_automation(self, task_id: int):
        db = SessionLocal()
        try:
            execution_service.run_task(db, task_id)
        finally:
            db.close()


automation_service = AutomationService()
