import uuid
import sqlalchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION
from .base import Base
from decimal import Decimal

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    event_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    amount: Mapped[Decimal] = mapped_column(DOUBLE_PRECISION, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)