import uuid
import datetime
from typing import Any, Dict
from pydantic import BaseModel, Field

class Event(BaseModel):
    id: uuid.UUID = Field(...)
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    date: datetime.date = Field(...)
    venue_id: uuid.UUID = Field(...)
    price: float = Field(0)
    content: Dict[str, Any] | None = None
