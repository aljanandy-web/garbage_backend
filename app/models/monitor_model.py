from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class Monitor(Base):
    __tablename__ = "monitors"

    id = Column(Integer, primary_key=True, index=True)
    monitor_id = Column(String, unique=True, index=True)
    driver_name = Column(String)
    status = Column(String)