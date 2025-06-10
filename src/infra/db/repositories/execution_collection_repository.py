from sqlalchemy.dialects.postgresql import insert as insert_db

from src.infra.db.settings.conection import DBconnectionHandler
from src.infra.db.interfaces.execution_collection_repository import ExecutionCollectionRepositoryInterface
from src.infra.db.entities.execution_collection import ExecutionCollection as ExecutionCollectionModel

class ExecutionCollectionRepository(ExecutionCollectionRepositoryInterface):

    def get_last_executation(self):
        try:
            with DBconnectionHandler() as db_connection:
                data = db_connection.session.query(
                    ExecutionCollectionModel.system,
                    ExecutionCollectionModel.last_executation
                ).all()
                return data
            
        except Exception as exception:
            raise exception