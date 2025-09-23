from sqlalchemy import Column, Integer, String, UniqueConstraint
from src.infra.db.settings.base import Base

class TicketsRequests(Base):
    __tablename__ = "tickets_requests"

    __table_args__ = (
        UniqueConstraint('ticket_id', 'system', name='uq_task_departament'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(String(100))
    code = Column(Integer)
    create_date = Column(String)
    departament = Column(String(100))
    status = Column(String(50))
    type = Column(String(50))
    due_date = Column(String, nullable=True)
    system = Column(String)
    conclusion_date = Column(String, nullable=True)
    responsible = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "code": self.code,
            "create_date": self.create_date,
            "departament": self.departament,
            "status": self.status,
            "type": self.type,
            "due_date": self.due_date,
            "system": self.system,
            "conclusion_date": self.conclusion_date,
            "responsible": self.responsible,
        }
