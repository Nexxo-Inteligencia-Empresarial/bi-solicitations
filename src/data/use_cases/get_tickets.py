from datetime import datetime, date
from typing import Optional, List
from collections import Counter
import pytz

from src.data.use_cases.interface.get_tickets import GetTickets as GetTicketsInterface
from src.infra.db.interfaces.tickets_requests_repository import TicketsRequestsRepositoryInterface
from src.data.factory.process_solicitations import *

class GetTickets(GetTicketsInterface):
    def __init__(self, repository: TicketsRequestsRepositoryInterface):
        self.__repository = repository


    def get_open_tickets(self, ft_dpt:Optional[List[str]] = None, ft_stts:Optional[List[str]] = None, total: bool = False):

        today = self.__today()
        rows = self.__repository.get_open_tickets(today)
        rows = [ row.to_dict() for row in rows]

        if total:
            open_tickets = process_open_tickets(rows, ft_dpt, ft_stts)
            return Counter(ticket['Status'] for ticket in open_tickets)

        return process_open_tickets(rows, ft_dpt, ft_stts)


    def get_by_departament(self, ft_dpt:Optional[List[str]] = None):

        today = self.__today()
        rows = self.__repository.get_tickets_departaments(today)
        data_expired = self.__repository.get_expired_tickets(today)

        rows = [tuple(r) for r in rows]
        data_expired = [tuple(d) for d in data_expired]

        return process_tickets(rows, data_expired, ft_dpt)


    def sla_per_month(self, departament_selected: Optional[List[str]] = None, start_date: Optional[date] = None, end_date: Optional[date] = None):

        rows = self.__get_tickets_to_sla_dashboard(start_date, end_date)
        rows = [ row.to_dict() for row in rows]

        return process_sla_per_month(rows, departament_selected)

    def get_sla(self, departament_selected: Optional[List[str]] = None, start_date: Optional[date] = None, end_date: Optional[date] = None):

        rows = self.__get_tickets_to_sla_dashboard(start_date, end_date)
        rows = [ row.to_dict() for row in rows]

        return process_general_sla(rows, departament_selected)

    def get_sla_exceded(self, departament_selected: Optional[List[str]] = None, start_date: Optional[date] = None, end_date: Optional[date] = None):

        rows = self.__get_tickets_to_sla_dashboard(start_date, end_date)
        rows = [ row.to_dict() for row in rows]

        return process_exceded_sla(rows, departament_selected)

    def __today(self):

        brazil_timezone = pytz.timezone('America/Sao_Paulo')
        now_brazil = datetime.now(brazil_timezone).date()
        today = now_brazil.isoformat()

        return today

    def __get_tickets_to_sla_dashboard(self, start_date=None, end_date=None):
        today = date.today()

        if start_date is None or end_date is None or start_date > end_date:
            start_date = date(today.year, 1, 1)
            end_date = today

        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

        rows = self.__repository.get_conclued_tickets(start_date, end_date)

        return rows
