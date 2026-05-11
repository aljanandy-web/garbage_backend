from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String) 
    start_point = Column(String)
    end_point = Column(String)
    assigned_truck_id = Column(Integer)