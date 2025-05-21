import time

from sqlalchemy.dialects.postgresql import insert as insert_db

from src.infra.db.settings.conection import DBconnectionHandler
from src.infra.db.entities.tickets_requests import TicketsRequests as TicketsRequestsModel
from src.infra.db.interfaces.tickets_requests_repository import TicketsRequestsRepositoryInterface

from src.domain.models.solicitation import Solicitation


class TicketsRequestsRepository(TicketsRequestsRepositoryInterface):
    def insert(self, solicitation: Solicitation) -> None:
        try:
            time.sleep(0.5)
            
            with DBconnectionHandler() as db_connection:
                stmt = insert_db(TicketsRequestsModel).values(
                    ticket_id=solicitation.ticket_id,
                    code=solicitation.code,
                    create_date=solicitation.create_date,
                    departament=solicitation.departament,
                    status=solicitation.status,
                    type=solicitation.type,
                    due_date=solicitation.due_date,
                    system=solicitation.system
                )

                update_dict = {
                    "code": solicitation.code,
                    "create_date": solicitation.create_date,
                    "status": solicitation.status,
                    "type": solicitation.type,
                    "due_date": solicitation.due_date
                }

                stmt = stmt.on_conflict_do_update(
                    index_elements=['ticket_id', 'system'],
                    set_=update_dict
                )

                db_connection.session.execute(stmt)
                db_connection.session.commit()                
        except Exception as exception:
            db_connection.session.rollback()
            raise exception