from pydantic import BaseModel

class ScheduleBase(BaseModel):
    title: str
    collection_time: str
    area: str
    status: str

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: int

    class Config:
        from_attributes = True