from abc import abstractmethod, ABC

class GetEmployeeticketsInterface(ABC):

    @abstractmethod
    def get_tickets(self, employee: str | None = None, start_date: str | None = None, end_date: str | None = None):
        raise Exception("'get_tickets' must be implemented")

    @abstractmethod
    def get_employees(self):
        raise Exception("'get_employees' must be implemented")
