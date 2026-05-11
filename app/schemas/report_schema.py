from pydantic import BaseModel

class ReportBase(BaseModel):
    issue_type: str
    description: str
    location: str

class ReportCreate(ReportBase):
    pass

class ReportResponse(ReportBase):
    id: int
    status: str

    class Config:
        from_attributes = True