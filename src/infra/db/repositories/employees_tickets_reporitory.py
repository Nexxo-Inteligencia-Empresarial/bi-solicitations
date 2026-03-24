from sqlalchemy import and_, func

from src.infra.db.entities.tickets_requests import TicketsRequests as TicketsRequestsModel
from src.infra.db.interfaces.employees_tickets_repository import EmployeesTicketsRepositoryInterface
from src.infra.db.settings.conection import DBconnectionHandler

class EmployeesTicketsRepository(EmployeesTicketsRepositoryInterface):

    def get_responded_tickets_by_employee(
        self,
        employee: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None
    ):

        try:
            with DBconnectionHandler() as db_connection:
                query = db_connection.session.query(TicketsRequestsModel).filter(
                    TicketsRequestsModel.status == "Respondida"
                )

                if employee:
                    query = query.filter(
                        func.lower(TicketsRequestsModel.responsible) == employee.lower()
                    )

                if start_date and end_date:
                    query = query.filter(
                        and_(
                            TicketsRequestsModel.conclusion_date >= start_date,
                            TicketsRequestsModel.conclusion_date <= end_date
                        )
                    )

                tickets = query.all()

                return tickets

        except Exception as exception:
            raise exception

    def get_all_employees(self):
        try:
            with DBconnectionHandler() as db_connection:
                data = (
                    db_connection.session
                    .query(
                        func.lower(TicketsRequestsModel.responsible).label("employee")
                    )
                    .filter(TicketsRequestsModel.responsible.isnot(None),
                            TicketsRequestsModel.status == "Respondida"
                            )
                    .distinct()
                    .order_by(func.lower(TicketsRequestsModel.responsible))
                    .all()
                )

                return [row.employee for row in data]

        except Exception as exception:
            raise exception
