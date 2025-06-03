from abc import ABC, abstractmethod

class TicketsRequestsRepositoryInterface(ABC):

    @abstractmethod
    def get_tickets(self, today: str):
        pass

    @abstractmethod
    def get_tickets_departaments(self, today: str):
        pass