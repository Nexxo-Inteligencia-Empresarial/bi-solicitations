from datetime import datetime, date
from typing import Optional, List
from collections import Counter
import pytz

from src.data.use_cases.interface.get_tickets import GetTickets as GetTicketsInterface
from src.infra.db.interfaces.tickets_requests_repository import TicketsRequestsRepositoryInterface
from src.data.factory.process_solicitations import *

class GetTicketsSla():

    def __init__(self, repository: TicketsRequestsRepositoryInterface):
        self.__repository = repository
        self.__rows = None

    def set_dataset(self, start_date: Optional[date] = None, end_date: Optional[date] = None, categories: Optional[List[str]] = None):
        rows = self.__get_tickets_to_sla_dashboard(start_date, end_date, categories)
        self.__rows = [ row.to_dict() for row in rows]

    def sla_per_month(self, departament_selected: Optional[List[str]] = None):
        return process_sla_per_month(self.__rows, departament_selected)

    def get_sla(self, departament_selected: Optional[List[str]] = None):
        return process_general_sla(self.__rows, departament_selected)

    def get_sla_exceded(self, departament_selected: Optional[List[str]] = None):
        return process_exceded_sla(self.__rows, departament_selected)

    def __get_tickets_to_sla_dashboard(self, start_date=None, end_date=None, categories=None):
        today = date.today()

        if start_date is None or end_date is None or start_date > end_date:
            start_date = date(today.year, 1, 1)
            end_date = today

        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

        rows = self.__repository.get_conclued_tickets(start_date, end_date, categories)

        return rows
