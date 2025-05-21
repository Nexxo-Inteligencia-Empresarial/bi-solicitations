from src.infra.db.interfaces.tickets_requests_repository import TicketsRequestsRepositoryInterface

class GetTickets:
    def __init__(self, tickets_requests_repository: TicketsRequestsRepositoryInterface):
        self.tickets_requests_repository = tickets_requests_repository
    
    def get(self):
        labels = []
        values = []
        rows = self.tickets_requests_repository.get_tickets()
        for row in rows:
            labels.append(row[0])
            values.append(row[1])
        return labels, values        