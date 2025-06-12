
from src.infra.db.interfaces.execution_collection_repository import ExecutionCollectionRepositoryInterface

class GetLastExecution:

    def __init__(self, execution_collection_repository: ExecutionCollectionRepositoryInterface):
        self.__repository = execution_collection_repository
        
    def get(self):
        rows = self.__repository.get_last_executation()

        return rows