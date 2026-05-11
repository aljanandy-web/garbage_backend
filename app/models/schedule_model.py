from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String) 
    collection_time = Column(String)
    area = Column(String)
    status = Column(String, default="Scheduled")