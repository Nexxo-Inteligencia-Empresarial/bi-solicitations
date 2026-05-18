from collections import defaultdict
from datetime import date, datetime, time, timedelta

from src.infra.db.interfaces.employees_tickets_repository import EmployeesTicketsRepositoryInterface
from src.data.factory.process_solicitations import process_tickets_by_employee

class GetEmployeetickets():

    def __init__(self, repository: EmployeesTicketsRepositoryInterface):
        self.__repository = repository

    def get_tickets(self, employee: str | None = None, start_date: str | None = None, end_date: str | None = None):

        if start_date is None or end_date is None or start_date > end_date:
            today = date.today()
            start_date, end_date = today, today

        start_date = start_date - timedelta(days=1)
        end_date = end_date + timedelta(days=1)

        datas = self.__repository.get_responded_tickets_by_employee(employee = employee,
                                                                     start_date = start_date,
                                                                     end_date = end_date)

        return process_tickets_by_employee(datas)



    def get_employees(self):
        datas = self.__repository.get_all_employees()
        return datas
