import uuid
from typing import Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import * # type: ignore
from api.infrastructure.postgres.dbcontext import DBContext
from models.user import User
from api.infrastructure.postgres.users import User as UserModel

class UserRepository():
    def __init__(self, dbcontext: DBContext) -> None:
        self._dbcontext: DBContext = dbcontext

    def _to_entity(self, model: UserModel) -> User:
        user = User(
            id=model.id,
            first_name=model.firstname,
            last_name=model.lastname,
            email=model.email,
            password=model.password,
            username=model.username,
            isadmin=model.is_superuser
        )
        return user

    def _to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            firstname=entity.first_name,
            lastname=entity.last_name,
            email=entity.email,
            password=entity.password,
            username=entity.username,
            is_superuser=entity.isadmin
        )

    def add(self, user: User) -> User:  # type: ignore[override]
        session: Session = self._dbcontext.createSession()
        entity = self._to_model(user)
        entity.is_active = True
        session.add(entity)
        session.commit()
        session.close()
        return user

    def update(self, user: User) -> Optional[User]:  # type: ignore[override]
        session: Session = self._dbcontext.createSession()
        record = session.query(UserModel).filter(UserModel.id == user.id).first()
        if not record:
            session.close()
            return None
        record.lastname = user.last_name
        record.firstname = user.first_name
        record.email = user.email
        record.username = user.username
        record.password = user.password
        record.is_superuser = user.isadmin
        session.commit()
        session.close()
        return user

    def delete(self, id: uuid.UUID) -> None:
        session: Session = self._dbcontext.createSession()
        record = session.query(UserModel).filter(UserModel.id == id).first()
        if not record:
            session.close()
            return None
        session.delete(record)
        session.commit()
        session.close()
        return None

    def get_by_username(self, username: str) -> Optional[User]:
        session: Session = self._dbcontext.createSession()
        record = session.query(UserModel).filter(UserModel.username == username).first()
        session.close()
        if not record:
            return None
        entity = self._to_entity(record)
        return entity

    def get_by_email(self, email: str) -> Optional[User]:
        session: Session = self._dbcontext.createSession()
        record = session.query(UserModel).filter(UserModel.email == email).first()
        session.close()
        if not record:
            return None
        entity = self._to_entity(record)
        return entity

    def get_by_id(self, id: uuid.UUID) -> Optional[User]:
        session: Session = self._dbcontext.createSession()
        record = session.query(UserModel).filter(UserModel.id == id).first()
        session.close()
        if not record:
            return None
        entity = self._to_entity(record)
        return entity

    def getall(self) -> List[User]:
        response: List[User] = list()
        session: Session = self._dbcontext.createSession()
        query = select(UserModel)
        records = session.execute(query).fetchall()
        for record in records:
            entity: User = self._to_entity(record[0])
            if entity is not None:
                response.append(entity)
        return response

    def username_exists(self, username: str) -> bool:
        return self.get_by_username(username) is not None

    def email_exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None
