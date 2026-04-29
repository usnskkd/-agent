from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.started = False

    def start(self):
        if not self.started:
            self.scheduler.start()
            self.started = True

    def shutdown(self):
        if self.started:
            self.scheduler.shutdown(wait=False)
            self.started = False

    def add_or_replace_interval_job(self, job_id: str, func, minutes: int, args: list):
        self.scheduler.add_job(
            func=func,
            trigger=IntervalTrigger(minutes=minutes),
            args=args,
            id=job_id,
            replace_existing=True,
        )

    def remove_missing_jobs(self, valid_ids: set[str]):
        for job in self.scheduler.get_jobs():
            if job.id not in valid_ids:
                self.scheduler.remove_job(job.id)


scheduler_service = SchedulerService()
