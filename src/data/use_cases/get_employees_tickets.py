from collections import defaultdict

from src.infra.db.interfaces.employees_tickets_repository import EmployeesTicketsRepositoryInterface

class GetEmployeetickets():

    def __init__(self, repository: EmployeesTicketsRepositoryInterface):
        self.__repository = repository

    def get_tickets(self, employee: str | None = None, start_date: str | None = None, end_date: str | None = None):

        datas = self.__repository.get_responded_tickets_by_employee(employee = employee,
                                                                     start_date = start_date,
                                                                     end_date = end_date)

        result = defaultdict(lambda: {
            "solicitações": [],
            "total": 0
        })

        for ticket in datas:
            employee_name = ticket.responsible or "Não informado"

            result[employee_name]["solicitações"].append(ticket)
            result[employee_name]["total"] += 1

        return result

    def get_employees(self):
        datas = self.__repository.get_all_employees()
        return datas
