from fastapi import APIRouter
from app.models.user import User
from app.schemas.user import UserCreate
from app.db.crud_user import create_user

router = APIRouter()

@router.post("/register/")
async def register_user(user: UserCreate):
    await create_user(user)
    return {"message": "User registered successfully"}
