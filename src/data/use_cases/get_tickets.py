from datetime import datetime, date
from collections import defaultdict
from typing import Optional, List, Tuple
import pytz

from src.infra.db.interfaces.tickets_requests_repository import TicketsRequestsRepositoryInterface
from src.utils.map_categories import categories

class GetTickets:
    def __init__(self, tickets_requests_repository: TicketsRequestsRepositoryInterface):
        self.tickets_requests_repository = tickets_requests_repository
    
    def get(self):
        
        brazil_timezone = pytz.timezone('America/Sao_Paulo')
        now_brazil = datetime.now(brazil_timezone)
        today = now_brazil.isoformat()

        rows = self.tickets_requests_repository.get_tickets_departaments(today)

        status_totals = {"Resolvendo": 0, "Responder": 0}

        for status, departament, count in rows:
            category = self.__classify_departaments(departament)

            if category is None:
                continue

            if status in status_totals:
                status_totals[status] += count

        labels = list(status_totals.keys())
        values = list(status_totals.values())
        return labels, values

    def get_by_departament(self):

        brazil_timezone = pytz.timezone('America/Sao_Paulo')
        now_brazil = datetime.now(brazil_timezone)

        today = now_brazil.isoformat()

        rows = self.tickets_requests_repository.get_tickets_departaments(today)

        datas = defaultdict(lambda: {"Resolvendo": 0, "Responder": 0})
        
        for status, departament, count in rows:
            category = self.__classify_departaments(departament)
            
            if category is None:
                continue

            datas[category][status] += count

        return dict(datas)
    
    def get_tickets_dates(self):

        data = self.tickets_requests_repository.get_tickets_dates()

        status_totals = {"Dentro do SLA": 0, "Fora do SLA": 0}

        for conclusion_date, create_date, _ in data:
            create_date = datetime.fromisoformat(create_date).date()
            conclusion_date = datetime.fromisoformat(conclusion_date).date()

            dias = (conclusion_date - create_date).days

            if dias <= 2:
                status_totals["Dentro do SLA"] += 1
            else:
                status_totals["Fora do SLA"] += 1

        labels = list(status_totals.keys())
        values = list(status_totals.values())
        return labels, values
    
    def get_tickets_dates_filters(self, departament_selected: Optional[List[str]] = None, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Tuple[List[str], List[int]]:

        data = self.tickets_requests_repository.get_tickets_dates()
        status_totals = {"Dentro do SLA": 0, "Fora do SLA": 0}

        for conclusion_date, create_date, departament in data:
            departament = self.__classify_departaments(departament.lower())
            create_date = datetime.fromisoformat(create_date).date()
            conclusion_date = datetime.fromisoformat(conclusion_date).date()

            if not self.__filter_departament(departament, departament_selected):
                continue
            
            if start_date and end_date:
                if not self.__filter_date(conclusion_date, start_date, end_date):
                    continue

            dias = (conclusion_date - create_date).days
            if dias <= 2:
                status_totals["Dentro do SLA"] += 1
            else:
                status_totals["Fora do SLA"] += 1

        labels = list(status_totals.keys())
        values = list(status_totals.values())
        return labels, values

    def __filter_departament(self, departament: str, selected: Optional[List[str]]) -> bool:
        if selected is None or not selected:
            return True
        return departament in selected

    def __filter_date(self, conclusion_date: date, start: Optional[date], end: Optional[date]) -> bool:
        if start and conclusion_date < start:
            return False
        if end and conclusion_date > end:
            return False
        return True
  
    def __classify_departaments(self, departament):
        for category, rules in categories.items():
            if departament in rules:
                return category
        return None
