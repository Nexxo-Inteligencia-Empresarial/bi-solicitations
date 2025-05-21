from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint
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
    due_date = Column(DateTime, nullable=True)
    system = Column(DateTime)
    
