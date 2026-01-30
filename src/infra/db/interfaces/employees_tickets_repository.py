from abc import ABC, abstractmethod

class EmployeesTicketsRepositoryInterface(ABC):

    @abstractmethod
    def get_responded_tickets_by_employee(
        self,
        employee: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None
    ):
        raise Exception("'get_responded_tickets_by_employee' must be implemented")

    @abstractmethod
    def get_all_employees(self):
        raise Exception("'get_all_employees' must be implemented")
