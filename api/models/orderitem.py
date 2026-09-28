import uuid
from pydantic import BaseModel, Field

class OrderItem(BaseModel):
    id: uuid.UUID = Field(...)
    order_id: uuid.UUID = Field(...)
    ticket_type_id: uuid.UUID = Field(...)
    quantity: int = Field(0)
    price: float = Field(0)