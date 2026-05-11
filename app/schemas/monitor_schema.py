from pydantic import BaseModel

class MonitorBase(BaseModel):
    monitor_id: str
    driver_name: str
    status: str

class MonitorCreate(MonitorBase):
    pass

class MonitorResponse(MonitorBase):
    id: int

    class Config:
        from_attributes = True