from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AutomationCreate(BaseModel):
    task_id: int
    name: str = Field(..., min_length=2, max_length=100)
    interval_minutes: int = Field(default=60, ge=1, le=10080)
    enabled: bool = True


class AutomationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    name: str
    interval_minutes: int
    enabled: bool = Field(validation_alias="enabled_bool")
    created_at: datetime
