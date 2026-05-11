from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.user_model import User
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Schema para sa Login Input
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    # 1. Hanapin ang user gamit ang email na input ni Aljan o Mickie
    user = db.query(User).filter(User.email == data.email).first()
    
    # 2. I-check kung nage-exist ang user at kung tama ang password
    if not user or user.password != data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Maling email o password."
        )
    
    # 3. Kung tama, ibalik ang user info para maka-pasok sa Dashboard
    return {
        "message": "Login Successful",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "role": "Admin" # O kahit anong default role niyo
        }
    }

@router.post("/logout")
def logout():
    return {"message": "Logout successful. Session cleared."}