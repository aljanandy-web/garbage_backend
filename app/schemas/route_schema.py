from pydantic import BaseModel
from typing import Optional

class RouteBase(BaseModel):
    route_name: str
    start_point: str
    end_point: str
    assigned_truck_id: Optional[int] = None

class RouteCreate(RouteBase):
    pass

class RouteResponse(RouteBase):
    id: int

    class Config:
        from_attributes = True