from datetime import datetime
from collections import defaultdict
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

        for conclusion_date, create_date in data:

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

  
    def __classify_departaments(self, departament):
        for category, rules in categories.items():
            if departament in rules:
                return category
        return None
