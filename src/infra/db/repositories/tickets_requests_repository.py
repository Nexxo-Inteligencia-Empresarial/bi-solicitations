from sqlalchemy import func, or_, and_

from src.infra.db.settings.conection import DBconnectionHandler
from src.infra.db.entities.tickets_requests import TicketsRequests as TicketsRequestsModel
from src.infra.db.interfaces.tickets_requests_repository import TicketsRequestsRepositoryInterface

class TicketsRequestsRepository(TicketsRequestsRepositoryInterface):
    def get_tickets(self, today: str):
        try:
            with DBconnectionHandler() as db_connection:
                data = db_connection.session.\
                    query(TicketsRequestsModel.status, func.count(TicketsRequestsModel.id)).\
                    filter(or_(
                        and_(
                            TicketsRequestsModel.status != "Respondida",
                            TicketsRequestsModel.due_date <= today

                        ),
                        and_(
                            TicketsRequestsModel.status != "Respondida",
                            TicketsRequestsModel.due_date == None

                        )
                    )).\
                    group_by(TicketsRequestsModel.status).\
                    all()

                return data
        except Exception as exception:
            raise exception
    
    def get_tickets_departaments(self, today: str):
        try:
            with DBconnectionHandler() as db_connection:
                data = db_connection.session.\
                    query(TicketsRequestsModel.status, func.lower(TicketsRequestsModel.departament).label("departament") ,func.count(TicketsRequestsModel.id)).\
                    filter(or_(
                        and_(
                            TicketsRequestsModel.status != "Respondida",
                            TicketsRequestsModel.due_date <= today

                        ),
                        and_(
                            TicketsRequestsModel.status != "Respondida",
                            TicketsRequestsModel.due_date == None

                        )
                    )).\
                    group_by(func.lower(TicketsRequestsModel.departament),
                             TicketsRequestsModel.status).\
                    all()
                
                return data
        except Exception as exception:
            raise exception
