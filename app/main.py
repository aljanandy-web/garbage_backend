from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database.connection import engine, Base, SessionLocal

# Import Models para mabilang ang data para sa Dashboard boxes
from app.models.user_model import User
from app.models.report_model import Report
from app.models.schedule_model import Schedule
from app.models.monitor_model import Monitor


from app.controllers import (
    auth_controller,  
    user_controller, 
    report_controller, 
    schedule_controller, 
    monitor_controller, 
    route_controller, 
    notification_controller
)

# Awtomatikong paggawa ng tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Waste Management System API",
    description="Backend logic supporting the Dashboard UI",
    version="1.0.0"
)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Register All Routers
app.include_router(auth_controller.router) 
app.include_router(user_controller.router)
app.include_router(report_controller.router)
app.include_router(schedule_controller.router)
app.include_router(monitor_controller.router)
app.include_router(route_controller.router)
app.include_router(notification_controller.router)


@app.get("/", tags=["Home / Dashboard"])
def get_home_dashboard(db: Session = Depends(get_db)):
    """
    Ito ang endpoint para sa 'Home' icon. 
    Nagbibigay ito ng summary data para sa apat na malalaking boxes sa UI.
    """
    return {
        "status": "Online",
        "developers": ["Nurusman Nasser", "Aljan Andy", "Mickie Cornelio"],
        "dashboard_stats": {
            "today_schedule": f"{db.query(Schedule).count()} Collections",
            "pending_reports": f"{db.query(Report).count()} Reports",
            "collected_status": "85% Complete",
            "active_trucks": f"{db.query(Monitor).count()}/6 Trucks"
        },
        "message": "Welcome to Smart Waste Dashboard API"
    }