from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    issue_type = Column(String) # Halimbawa: 'Overflowing Bin'
    description = Column(String)
    location = Column(String)
    status = Column(String, default="Pending") # Pending, In-Progress, Resolved