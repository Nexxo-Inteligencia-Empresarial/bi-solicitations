from abc import ABC, abstractmethod

class TicketsRequestsRepositoryInterface(ABC):

    @abstractmethod
    def get_tickets(self, create_date: str):
        pass