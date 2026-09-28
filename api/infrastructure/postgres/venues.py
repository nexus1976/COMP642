import uuid
import sqlalchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION
from .base import Base
from decimal import Decimal

class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    capacity: Mapped[int] = mapped_column(sqlalchemy.Integer, nullable=False)

    def __repr__(self):
        return f"<Venue(id={self.id}, name={self.name}, address={self.address}, capacity={self.capacity})>"
    