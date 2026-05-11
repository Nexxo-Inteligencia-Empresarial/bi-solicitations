from sqlalchemy import Column, Integer, String, UniqueConstraint, Boolean
from src.infra.db.settings.base import Base

class TicketsRequests(Base):
    __tablename__ = "tickets_requests"

    __table_args__ = (
        UniqueConstraint('ticket_id', 'system', 'reopen', name='tickets_requests_unique'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(String(100), nullable=False)
    code = Column(Integer, nullable=True)
    create_date = Column(String(16), nullable=False)
    departament = Column(String(100), nullable=True)
    status = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    due_date = Column(String(10), nullable=True)
    system = Column(String(50), nullable=False)
    conclusion_date = Column(String(16), nullable=True)
    responsible = Column(String(100), nullable=True)
    shared = Column(Boolean, nullable=False, default=False)
    delivery_time = Column(String(16), nullable=True)
    reopen = Column(Integer, nullable=False)


    def to_dict(self):
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "create_date": self.create_date,
            "departament": self.departament,
            "status": self.status,
            "type": self.type,
            "due_date": self.due_date,
            "system": self.system,
            "conclusion_date": self.conclusion_date,
            "responsible": self.responsible,
            "delivery_time": self.delivery_time,
        }
