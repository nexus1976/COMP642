from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine

class DBContext:
    def __init__(self, host: str, dbname: str, username: str, password: str) -> None:
        if host and dbname and username and password:
            self._connectionString: str = f'postgresql://{username}:{password}@{host}:5432/{dbname}'
            self._engine: Engine = create_engine(self._connectionString, connect_args={'options': '-c timezone=utc'})
            self._session: sessionmaker = sessionmaker(bind=self._engine)
        else:
            self._connectionString: str = ''

    @property
    def connectionString(self) -> str:
        return self._connectionString
    
    @property
    def engine(self) -> Engine:
        return self._engine
    
    @property
    def session(self) -> sessionmaker:
        return self._session
    
    def createSession(self) -> Session:
        session: Session = self._session()
        return session