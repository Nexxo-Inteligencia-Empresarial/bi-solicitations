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

        labels = []
        values = []
        rows = self.tickets_requests_repository.get_tickets(today)
        for row in rows:
            labels.append(row[0])
            values.append(row[1])
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
    
    def __classify_departaments(self, departament):
        for category, rules in categories.items():
            if departament in rules:
                return category
        return None
