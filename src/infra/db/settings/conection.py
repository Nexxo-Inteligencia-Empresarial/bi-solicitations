from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.environment import settings

db_settings = settings.database

class DBconnectionHandler:
    def __init__(self) -> None:
        self.__conection_string = "{}://{}:{}@{}:{}/{}".format(
            'postgresql+psycopg2',
            db_settings.user,
            db_settings.password,
            db_settings.host,
            db_settings.port,
            db_settings.database,
        )
        self.__engine = self.__create_database_engine()
        self.session = None
        
    def __create_database_engine(self):
        engine = create_engine(self.__conection_string)
        return engine

    def get_engine(self):
        return self.__engine
    
    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    