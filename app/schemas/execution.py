from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ExecutionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    status: str
    result: dict
    started_at: datetime
