from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    goal: str = Field(..., min_length=3, max_length=300)
    channel: str = Field(..., min_length=2, max_length=80)
    audience: str = Field(..., min_length=2, max_length=120)
    budget: str = Field(default="small", max_length=80)
    metadata: dict = Field(default_factory=dict)


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    goal: str
    channel: str
    audience: str
    budget: str
    status: str
    metadata: dict = Field(validation_alias="metadata_json")
    created_at: datetime
