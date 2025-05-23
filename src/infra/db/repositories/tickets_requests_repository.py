from sqlalchemy import func, or_

from src.infra.db.settings.conection import DBconnectionHandler
from src.infra.db.entities.tickets_requests import TicketsRequests as TicketsRequestsModel
from src.infra.db.interfaces.tickets_requests_repository import TicketsRequestsRepositoryInterface

class TicketsRequestsRepository(TicketsRequestsRepositoryInterface):
    def get_tickets(self, create_date: str):
        try:
            with DBconnectionHandler() as db_connection:
                data = db_connection.session.\
                    query(TicketsRequestsModel.status, func.count(TicketsRequestsModel.id)).\
                    filter(or_(
                        TicketsRequestsModel.create_date == create_date,
                        TicketsRequestsModel.status != "Respondida"
                    )).\
                    group_by(TicketsRequestsModel.status).\
                    all()

                return data
        except Exception as exception:
            raise exception
