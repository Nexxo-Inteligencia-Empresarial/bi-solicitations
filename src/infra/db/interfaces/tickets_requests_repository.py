from abc import ABC, abstractmethod

class TicketsRequestsRepositoryInterface(ABC):

    @abstractmethod
    def get_tickets(self, today: str):
        pass