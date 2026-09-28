import uuid
import datetime
from pydantic import BaseModel, Field

class Event(BaseModel):
    id: uuid.UUID = Field(...)
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    date: datetime.date = Field(...)
    location: str = Field(..., min_length=1)
    price: float = Field(0)
