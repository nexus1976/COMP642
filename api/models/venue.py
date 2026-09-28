import uuid
from pydantic import BaseModel, Field

class Venue(BaseModel):
    id: uuid.UUID = Field(...)
    name: str = Field(..., min_length=1)
    address: str = Field(..., min_length=1)
    capacity: int = Field(0)
