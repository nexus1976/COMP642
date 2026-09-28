import uuid
import sqlalchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION
from .base import Base
from decimal import Decimal

class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    firstname: Mapped[str] = mapped_column(String(100))
    lastname: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(sqlalchemy.Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(sqlalchemy.Boolean, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"