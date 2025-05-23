from datetime import datetime
import pytz
from src.infra.db.interfaces.tickets_requests_repository import TicketsRequestsRepositoryInterface

class GetTickets:
    def __init__(self, tickets_requests_repository: TicketsRequestsRepositoryInterface):
        self.tickets_requests_repository = tickets_requests_repository
    
    def get(self):

        brazil_timezone = pytz.timezone('America/Sao_Paulo')
        now_brazil = datetime.now(brazil_timezone)

        create_date = now_brazil.isoformat()

        labels = []
        values = []
        rows = self.tickets_requests_repository.get_tickets(create_date)
        for row in rows:
            labels.append(row[0])
            values.append(row[1])
        return labels, values        