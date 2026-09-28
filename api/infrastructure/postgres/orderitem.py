import uuid
import sqlalchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION
from .base import Base
from decimal import Decimal

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    ticket_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    quantity: Mapped[int] = mapped_column(sqlalchemy.Integer, nullable=False)
    price: Mapped[Decimal] = mapped_column(DOUBLE_PRECISION, nullable=False)

    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, ticket_type_id={self.ticket_type_id}, quantity={self.quantity}, price={self.price})>"
    