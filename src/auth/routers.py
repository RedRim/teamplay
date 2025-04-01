from fastapi import APIRouter

from src.core.models import async_session_maker
from .models import UserBase, User

auth_router = APIRouter(prefix="/profile", tags=["profile"])


@auth_router.post("/users", response_model=User)
async def create_user(user_data: UserBase):
    async with async_session_maker() as session:
        user = User(**user_data.model_dump())
        session.add(user)
        await session.commit()
        await session.refresh(user)    
        return user