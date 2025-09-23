from datetime import datetime, date
from typing import Optional, List, Tuple
from collections import Counter
import pytz

from src.data.use_cases.interface.get_tickets import GetTickets as GetTicketsInterface
from src.infra.db.interfaces.tickets_requests_repository import TicketsRequestsRepositoryInterface
from src.data.factory.process_solicitations import *

class GetTickets(GetTicketsInterface):
    def __init__(self, tickets_requests_repository: TicketsRequestsRepositoryInterface):
        self.tickets_requests_repository = tickets_requests_repository


    def get_open_tickets(self, ft_dpt:Optional[List[str]] = None, ft_stts:Optional[List[str]] = None, total: bool = False):

        today = self.__today()
        rows = self.tickets_requests_repository.get_open_tickets(today)
        rows = [ row.to_dict() for row in rows]

        if total:
            open_tickets = process_open_tickets(rows, ft_dpt, ft_stts)
            return Counter(ticket['Status'] for ticket in open_tickets)

        return process_open_tickets(rows, ft_dpt, ft_stts)


    def get_by_departament(self, ft_dpt:Optional[List[str]] = None):

        today = self.__today()
        rows = self.tickets_requests_repository.get_tickets_departaments(today)
        data_expired = self.tickets_requests_repository.get_expired_tickets(today)

        rows = [tuple(r) for r in rows]
        data_expired = [tuple(d) for d in data_expired]

        return process_tickets(rows, data_expired, ft_dpt)


    def sla_per_month(self, departament_selected: Optional[List[str]] = None, start_date: Optional[date] = None, end_date: Optional[date] = None):

        rows = self.tickets_requests_repository.get_conclued_tickets()
        rows = [ row.to_dict() for row in rows]

        return process_sla_per_month(rows, departament_selected, start_date, end_date)

    def get_sla(self, departament_selected: Optional[List[str]] = None, start_date: Optional[date] = None, end_date: Optional[date] = None):

        rows = self.tickets_requests_repository.get_conclued_tickets()
        rows = [ row.to_dict() for row in rows]

        return process_general_sla(rows, departament_selected, start_date, end_date)

    def get_sla_exceded(self, departament_selected: Optional[List[str]] = None, start_date: Optional[date] = None, end_date: Optional[date] = None):

        rows = self.tickets_requests_repository.get_conclued_tickets()
        rows = [ row.to_dict() for row in rows]

        return process_exceded_sla(rows, departament_selected, start_date, end_date)

    def __today(self):

        brazil_timezone = pytz.timezone('America/Sao_Paulo')
        now_brazil = datetime.now(brazil_timezone).date()
        today = now_brazil.isoformat()

        return today
