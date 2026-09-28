import uuid
from pydantic import BaseModel, Field

class Order(BaseModel):
    id: uuid.UUID = Field(...)
    user_id: uuid.UUID = Field(...)
    event_id: uuid.UUID = Field(...)
    total_amount: float = Field(...)
    status: str = Field(..., min_length=1)
