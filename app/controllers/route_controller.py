from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.route_model import Route
from app.schemas.route_schema import RouteCreate, RouteResponse

router = APIRouter(prefix="/routes", tags=["Route Management"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[RouteResponse])
def get_routes(db: Session = Depends(get_db)):
    return db.query(Route).all()

@router.post("/", response_model=RouteResponse, status_code=201)
def create_route(route: RouteCreate, db: Session = Depends(get_db)):
    new_route = Route(**route.model_dump())
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    return new_route

@router.put("/{route_id}", response_model=RouteResponse)
def update_route(route_id: int, route_data: RouteCreate, db: Session = Depends(get_db)):
    db_route = db.query(Route).filter(Route.id == route_id).first()
    if not db_route:
        raise HTTPException(status_code=404, detail="Route not found")
    for key, value in route_data.model_dump().items():
        setattr(db_route, key, value)
    db.commit()
    db.refresh(db_route)
    return db_route

@router.delete("/{route_id}")
def delete_route(route_id: int, db: Session = Depends(get_db)):
    db_route = db.query(Route).filter(Route.id == route_id).first()
    if not db_route:
        raise HTTPException(status_code=404, detail="Route not found")
    db.delete(db_route)
    db.commit()
    return {"message": "Route deleted successfully"}