import uuid
import datetime
import sqlalchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION, DATE
from .base import Base
from decimal import Decimal

class Event(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    date: Mapped[datetime.date] = mapped_column(DATE, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(DOUBLE_PRECISION, nullable=False)

    def __repr__(self):
        return f"<Event(id={self.id}, name={self.name}, description={self.description}, date={self.date}, location={self.location}, price={self.price})>"