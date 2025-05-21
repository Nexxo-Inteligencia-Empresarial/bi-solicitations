from abc import ABC, abstractmethod

from src.domain.models.solicitation import Solicitation

class TicketsRequestsRepositoryInterface(ABC):

    @abstractmethod
    def insert(self, task: Solicitation) -> None:
        pass