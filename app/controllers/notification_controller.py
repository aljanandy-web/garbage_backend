from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.notification_model import Notification
from app.schemas.notification_schema import NotificationCreate, NotificationResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[NotificationResponse])
def get_notifications(db: Session = Depends(get_db)):
    return db.query(Notification).all()

@router.post("/", response_model=NotificationResponse, status_code=201)
def send_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    new_notif = Notification(**notification.model_dump())
    db.add(new_notif)
    db.commit()
    db.refresh(new_notif)
    return new_notif

@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification(notification_id: int, notification_data: NotificationCreate, db: Session = Depends(get_db)):
    db_notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not db_notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    for key, value in notification_data.model_dump().items():
        setattr(db_notif, key, value)
    db.commit()
    db.refresh(db_notif)
    return db_notif

@router.delete("/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not db_notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(db_notif)
    db.commit()
    return {"message": "Notification deleted successfully"}   