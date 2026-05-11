from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.monitor_model import Monitor
from app.schemas.monitor_schema import MonitorCreate, MonitorResponse

router = APIRouter(prefix="/monitors", tags=["Monitor Management"])

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. READ ALL (GET)
@router.get("/", response_model=list[MonitorResponse])
def get_monitors(db: Session = Depends(get_db)):
    return db.query(Monitor).all()

# 2. CREATE (POST)
@router.post("/", response_model=MonitorResponse, status_code=201)
def create_monitor(monitor: MonitorCreate, db: Session = Depends(get_db)):
    new_monitor = Monitor(**monitor.model_dump())
    db.add(new_monitor)
    db.commit()
    db.refresh(new_monitor)
    return new_monitor

# 3. UPDATE (PUT)
@router.put("/{id}", response_model=MonitorResponse)
def update_monitor(id: int, monitor_data: MonitorCreate, db: Session = Depends(get_db)):
    db_monitor = db.query(Monitor).filter(Monitor.id == id).first()
    if not db_monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")
    
    for key, value in monitor_data.model_dump().items():
        setattr(db_monitor, key, value)
    
    db.commit()
    db.refresh(db_monitor)
    return db_monitor

# 4. DELETE (DELETE)
@router.delete("/{id}")
def delete_monitor(id: int, db: Session = Depends(get_db)):
    db_monitor = db.query(Monitor).filter(Monitor.id == id).first()
    if not db_monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")
    
    db.delete(db_monitor)
    db.commit()
    return {"message": f"Monitor with ID {id} has been deleted"}