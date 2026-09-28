import uuid
from pydantic import BaseModel, Field

class TicketType(BaseModel):
    id: uuid.UUID = Field(...)
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    price: float = Field(0)
    