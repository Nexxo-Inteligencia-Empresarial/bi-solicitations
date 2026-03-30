from datetime import datetime, date, timedelta
from typing import Optional, List
from collections import Counter
import pytz

from src.infra.db.interfaces.tickets_requests_repository import TicketsRequestsRepositoryInterface
from src.data.factory.process_solicitations import *

class GetTickets():
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

    def get_by_create_date(self, start_date: Optional[date] = None, end_date: Optional[date] = None, categories: Optional[List[str]] = None):
        if start_date is None or end_date is None or start_date > end_date:
            today = date.today()
            start_date, end_date = today, today

        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

        start_date = start_date - timedelta(days=1) + timedelta(hours=18)
        start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")

        end_date = end_date + timedelta(hours=18)
        end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")

        rows = self.__repository.get_tickets_by_create_date(start_date, end_date, categories)
        datas =[ row.to_dict() for row in rows]

        return process_tickets_by_create_date(datas)

    def __today(self):

        brazil_timezone = pytz.timezone('America/Sao_Paulo')
        now_brazil = datetime.now(brazil_timezone).date()
        today = now_brazil.isoformat()

        return today
