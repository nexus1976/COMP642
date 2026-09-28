"""Shared plumbing for the model repositories.

Each repository accepts/returns the plain domain classes (``models/*.py``) and
persists them through the matching SQLAlchemy model (``orm/*.py``) using a
session created by ``DBContext``.

One session is opened per repository call and committed (or rolled back) when
the call finishes. Domain objects are built *inside* the session scope, so
nothing returned from a repository is a detached ORM instance.
"""
from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Generic, Iterator, List, Optional, Protocol, Type, TypeVar, Union

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api.infrastructure.postgres.dbcontext import DBContext

IdLike = Union[str, uuid.UUID]


class _HasId(Protocol):
    id: uuid.UUID


TEntity = TypeVar("TEntity", bound=_HasId)
TModel = TypeVar("TModel")


def to_uuid(value: IdLike) -> uuid.UUID:
    """The domain classes use ``str`` for foreign keys, the ORM uses ``UUID``."""
    return value if isinstance(value, uuid.UUID) else uuid.UUID(str(value))


class BaseRepository(ABC, Generic[TEntity, TModel]):
    model_class: Type[TModel]

    def __init__(self, db_context: DBContext) -> None:
        self._db = db_context

    # ------------------------------------------------------------------
    # Session handling
    # ------------------------------------------------------------------
    @contextmanager
    def _session_scope(self) -> Iterator[Session]:
        session = self._db.createSession()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    # ------------------------------------------------------------------
    # Mapping hooks (implemented by each repository)
    # ------------------------------------------------------------------
    @abstractmethod
    def _to_entity(self, model: TModel) -> TEntity:
        """ORM model -> domain object."""

    @abstractmethod
    def _to_model(self, entity: TEntity, **extras: Any) -> TModel:
        """Domain object -> new ORM model (``extras`` = columns the domain class lacks)."""

    @abstractmethod
    def _apply(self, model: TModel, entity: TEntity, **extras: Any) -> None:
        """Copy domain object values onto an existing ORM model."""

    # ------------------------------------------------------------------
    # Generic CRUD
    # ------------------------------------------------------------------
    def add(self, entity: TEntity, **extras: Any) -> TEntity:
        with self._session_scope() as session:
            model = self._to_model(entity, **extras)
            session.add(model)
            session.flush()
            return self._to_entity(model)

    def get_by_id(self, entity_id: IdLike) -> Optional[TEntity]:
        with self._session_scope() as session:
            model = session.get(self.model_class, to_uuid(entity_id))
            return self._to_entity(model) if model is not None else None

    def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[TEntity]:
        with self._session_scope() as session:
            stmt = (
                select(self.model_class)
                .order_by(self.model_class.id)  # type: ignore[attr-defined]
                .offset(offset)
            )
            if limit is not None:
                stmt = stmt.limit(limit)
            return [self._to_entity(m) for m in session.scalars(stmt)]

    def update(self, entity: TEntity, **extras: Any) -> Optional[TEntity]:
        """Returns the updated entity, or ``None`` if no row has that id."""
        with self._session_scope() as session:
            model = session.get(self.model_class, entity.id)
            if model is None:
                return None
            self._apply(model, entity, **extras)
            session.flush()
            return self._to_entity(model)

    def delete(self, entity_id: IdLike) -> bool:
        """Returns ``True`` if a row was deleted."""
        with self._session_scope() as session:
            model = session.get(self.model_class, to_uuid(entity_id))
            if model is None:
                return False
            session.delete(model)
            return True

    def exists(self, entity_id: IdLike) -> bool:
        with self._session_scope() as session:
            return session.get(self.model_class, to_uuid(entity_id)) is not None

    def count(self) -> int:
        with self._session_scope() as session:
            return session.scalar(select(func.count()).select_from(self.model_class)) or 0

    # ------------------------------------------------------------------
    # Helpers for subclass finders
    # ------------------------------------------------------------------
    def _find(self, *criteria: Any) -> List[TEntity]:
        with self._session_scope() as session:
            stmt = select(self.model_class).where(*criteria)
            return [self._to_entity(m) for m in session.scalars(stmt)]

    def _find_one(self, *criteria: Any) -> Optional[TEntity]:
        with self._session_scope() as session:
            stmt = select(self.model_class).where(*criteria)
            model = session.scalars(stmt).first()
            return self._to_entity(model) if model is not None else None