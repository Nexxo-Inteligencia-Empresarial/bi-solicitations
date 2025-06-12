from sqlalchemy import Column, Integer, String, TIMESTAMP
from src.infra.db.settings.base import Base

class ExecutionCollection(Base):
    __tablename__ = "execution_collection"
    
    last_executation = Column(TIMESTAMP, nullable=False)
    system = Column(String(50), nullable=False,  primary_key=True)
