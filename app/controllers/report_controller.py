from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.report_model import Report
from app.schemas.report_schema import ReportCreate, ReportResponse

router = APIRouter(prefix="/reports", tags=["Reports"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ReportResponse])
def get_reports(db: Session = Depends(get_db)):
    return db.query(Report).all()

@router.post("/", response_model=ReportResponse, status_code=201)
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    new_report = Report(**report.model_dump())
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

@router.put("/{report_id}", response_model=ReportResponse)
def update_report(report_id: int, report_data: ReportCreate, db: Session = Depends(get_db)):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    for key, value in report_data.model_dump().items():
        setattr(db_report, key, value)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.delete("/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    db.delete(db_report)
    db.commit()
    return {"message": "Report deleted successfully"}