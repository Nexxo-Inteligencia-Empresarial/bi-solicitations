from abc import ABC, abstractmethod

class TicketsRequestsRepositoryInterface(ABC):

    @abstractmethod
    def get_tickets_departaments(self, today: str):
        pass

    @abstractmethod
    def get_tickets_dates(self):
        pass

    @abstractmethod
    def get_tickets_expired(self, today: str):
        pass
