from abc import ABC, abstractmethod
from typing import List

from src.infra.db.entities.tickets_requests import TicketsRequests

class TicketsRequestsRepositoryInterface(ABC):

    @abstractmethod
    def get_tickets_departaments(self, today: str):
        pass

    @abstractmethod
    def get_expired_tickets(self, today: str):
        pass

    @abstractmethod
    def get_conclued_tickets(self) -> List[TicketsRequests]:
        pass

    @abstractmethod
    def get_open_tickets(self, today: str) -> List[TicketsRequests]:
        pass
