import uuid
from typing import List
from pydantic import BaseModel, Field
from api.models.orderitem import OrderItem

class Order(BaseModel):
    id: uuid.UUID = Field(...)
    user_id: uuid.UUID = Field(...)
    event_id: uuid.UUID = Field(...)
    total_amount: float = Field(...)
    status: str = Field(..., min_length=1)
    order_items: List[OrderItem] = Field(default_factory=list)
