from datetime import datetime, time
import pytz

from sqlalchemy import func, or_, and_, cast, Date

from src.infra.db.settings.conection import DBconnectionHandler
from src.infra.db.entities.tickets_requests import TicketsRequests as TicketsRequestsModel
from src.infra.db.interfaces.tickets_requests_repository import TicketsRequestsRepositoryInterface

class TicketsRequestsRepository(TicketsRequestsRepositoryInterface):

    def get_tickets_departaments(self, today: str):
        today_18h = self.__get_today_utc_18h()
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
                            TicketsRequestsModel.create_date <= today_18h.strftime('%Y-%m-%d %H:%M')
                        ),
                        and_(
                            ~TicketsRequestsModel.create_date.contains(' '),
                            cast(TicketsRequestsModel.create_date, Date) <= today_18h.date()
                        )
                    )
                ).group_by(
                    func.lower(TicketsRequestsModel.departament),
                    TicketsRequestsModel.status
                ).all()
                return data
        except Exception as exception:
            raise exception

    def get_tickets_dates(self):
        with DBconnectionHandler() as db_connection:
            try:
                data = db_connection.session.\
                    query(
                        TicketsRequestsModel.conclusion_date,
                        TicketsRequestsModel.create_date,
                        TicketsRequestsModel.departament,
                        TicketsRequestsModel.ticket_id,
                        TicketsRequestsModel.system,
                        TicketsRequestsModel.type,
                        TicketsRequestsModel.due_date
                    ).\
                    filter(TicketsRequestsModel.conclusion_date.isnot(None))

                return data.all()

            except Exception as exception:
                raise exception

    def get_tickets_expired(self, today: str):
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

    def get_tickets_full(self, today: str):
        today_18h = self.__get_today_utc_18h()
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
                            TicketsRequestsModel.create_date <= today_18h.strftime('%Y-%m-%d %H:%M')
                        ),
                        and_(
                            ~TicketsRequestsModel.create_date.contains(' '),
                            cast(TicketsRequestsModel.create_date, Date) <= today_18h.date()
                        )
                    )
                ).all()
                return data
        except Exception as exception:
            raise exception

    def __get_today_utc_18h(self):
        br_tz = pytz.timezone("America/Sao_Paulo")
        today_18h_br = br_tz.localize(datetime.now().replace(hour=18, minute=0, second=0, microsecond=0))
        today_18h_utc = today_18h_br.astimezone(pytz.UTC)
        return today_18h_utc
