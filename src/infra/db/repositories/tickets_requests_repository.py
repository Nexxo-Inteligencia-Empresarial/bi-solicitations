from datetime import datetime
import pytz

from sqlalchemy import func, or_, and_, cast, Date

from src.infra.db.settings.conection import DBconnectionHandler
from src.infra.db.entities.tickets_requests import TicketsRequests as TicketsRequestsModel
from src.infra.db.interfaces.tickets_requests_repository import TicketsRequestsRepositoryInterface

class TicketsRequestsRepository(TicketsRequestsRepositoryInterface):

    def get_tickets_departaments(self, today: str):
        deadline = self.__deadline()
        try:
            with DBconnectionHandler() as db_connection:
                data = db_connection.session.query(
                    TicketsRequestsModel.status,
                    func.lower(TicketsRequestsModel.departament).label("departament"),
                    func.count(TicketsRequestsModel.id)
                ).filter(or_(
                    and_(
                        TicketsRequestsModel.status != "Respondida",
                        TicketsRequestsModel.due_date <= today
                    ),
                    and_(
                        TicketsRequestsModel.status != "Respondida",
                        TicketsRequestsModel.due_date == None
                    )
                )).filter(
                    or_(
                        and_(
                            TicketsRequestsModel.create_date.contains(' '),
                            TicketsRequestsModel.create_date <= deadline.strftime('%Y-%m-%d %H:%M')
                        ),
                        and_(
                            ~TicketsRequestsModel.create_date.contains(' '),
                            cast(TicketsRequestsModel.create_date, Date) <= deadline.date()
                        )
                    )
                ).group_by(
                    func.lower(TicketsRequestsModel.departament),
                    TicketsRequestsModel.status
                ).all()
                return data
        except Exception as exception:
            raise exception

    def get_conclued_tickets(self):
        with DBconnectionHandler() as db_connection:
            try:
                data = db_connection.session.\
                    query(TicketsRequestsModel).\
                    filter(TicketsRequestsModel.conclusion_date.isnot(None))

                return data.all()

            except Exception as exception:
                raise exception

    def get_open_tickets(self, today: str):
        deadline = self.__deadline()
        try:
            with DBconnectionHandler() as db_connection:
                data = db_connection.session.query(
                    TicketsRequestsModel
                ).filter(or_(
                    and_(
                        TicketsRequestsModel.status != "Respondida",
                        TicketsRequestsModel.due_date <= today
                    ),
                    and_(
                        TicketsRequestsModel.status != "Respondida",
                        TicketsRequestsModel.due_date == None
                    )
                )).filter(
                    or_(
                        and_(
                            TicketsRequestsModel.create_date.contains(' '),
                            TicketsRequestsModel.create_date <= deadline.strftime('%Y-%m-%d %H:%M')
                        ),
                        and_(
                            ~TicketsRequestsModel.create_date.contains(' '),
                            cast(TicketsRequestsModel.create_date, Date) <= deadline.date()
                        )
                    )
                ).all()
                return data
        except Exception as exception:
            raise exception

    def get_expired_tickets(self, today: str):
        try:
            with DBconnectionHandler() as db_connection:
                data = db_connection.session.query(
                    func.lower(TicketsRequestsModel.departament).label("departament"),
                    func.count(TicketsRequestsModel.id).label("total_atrasados")
                ).filter(
                      and_(
                            TicketsRequestsModel.status == "Resolvendo",
                            TicketsRequestsModel.due_date < today
                        )
                ).group_by(
                    func.lower(TicketsRequestsModel.departament)
                ).all()

                return data
        except Exception as exception:
            raise exception

    def __deadline(self):
        br_tz = pytz.timezone("America/Sao_Paulo")
        now = datetime.now(br_tz)

        limit = 17 if now.weekday() == 4 else 18

        deadline = now.replace(hour=limit, minute=0, second=0, microsecond=0)
        deadline_utc = deadline.astimezone(pytz.UTC)

        return deadline_utc
