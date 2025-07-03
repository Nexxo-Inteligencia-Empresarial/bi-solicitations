from abc import ABC, abstractmethod

class ExecutionCollectionRepositoryInterface(ABC):

    @abstractmethod
    def get_last_executation(self):
        raise Exception("'get_last_executation' must be implemented")
