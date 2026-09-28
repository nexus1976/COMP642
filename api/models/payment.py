import uuid
from pydantic import BaseModel, Field

class Payment(BaseModel):
    id: uuid.UUID = Field(...)
    user_id: uuid.UUID = Field(...)
    order_id: uuid.UUID = Field(...)
    amount: float = Field(0)
    status: str = Field(..., min_length=0)
