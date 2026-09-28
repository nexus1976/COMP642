import uuid
import sqlalchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION
from .base import Base
from decimal import Decimal

class TicketType(Base):
    __tablename__ = "ticket_types"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    price: Mapped[Decimal] = mapped_column(DOUBLE_PRECISION, nullable=False)

    def __repr__(self):
        return f"<TicketType(id={self.id}, name={self.name}, description={self.description}, price={self.price})>"