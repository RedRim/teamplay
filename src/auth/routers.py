from typing import Union
from fastapi import APIRouter, HTTPException

from src.core.models import async_session_maker
from .models import (
    UserBase,
    User,
    Profile,
) 
from sqlmodel import select

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/user/create", response_model=User)
async def create_user(data: UserBase):
    async with async_session_maker() as session:
        print(data.model_dump())
        user = User(**data.model_dump())
        profile = Profile(user=user)
        session.add(user)
        session.add(profile)
        await session.commit()

        return user


@auth_router.get("/user", response_model=list[UserBase])
async def get_user():
    async with async_session_maker() as session:
        query = select(User)
        results = await session.exec(query)
        instances = results.all()

        return instances
    

@auth_router.get("/user/{id}", response_model=Union[User, None])
async def get_user(id: int):
    model = User
    async with async_session_maker() as session:
        query = select(model).where(model.id == id)
        result = await session.exec(query)
        instance = result.one_or_none()
        if instance is None:
            raise HTTPException(status_code=404, detail=f"Не найдено записи в таблице {model.__name__} с {id=}")

        return instance


@auth_router.patch("/user/{id}", response_model=Union[User, None])
async def update_user(id: int, data: UserBase):
    model = User
    async with async_session_maker() as session:
        query = select(model).where(model.id == id)
        result = await session.exec(query)
        instance = result.one_or_none()
        if instance is None:
            raise HTTPException(status_code=404, detail=f"Не найдено записи в таблице {model.__name__} с {id=}")
        test = data.model_dump(exclude_unset=False)
        test_2 = data.model_dump(exclude_unset=True)
        print(test)
        print(test_2)

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, key, value)
        
        session.add(instance)
        session.commit()

        return instance
    
@auth_router.delete("user/{id}", response_model=dict)
async def delete_user(id: int):
    model = User
    async with async_session_maker() as session:
        query = select(model).where(model.id == id)
        result = await session.exec(query)
        instance = result.one_or_none()
        if instance is None:
            raise HTTPException(status_code=404, detail=f"Не найдено записи в таблице {model.__name__} c {id=}")
        profile_query = select(Profile).where(Profile.user_id==instance.id)
        profile = await session.exec(profile_query)
        profile_instance = profile.one_or_none()
        if profile_instance:
            await session.delete(profile_instance)
        await session.delete(instance)
        await session.commit()

        return {"success": f"Запись {model.__name__} c {id=} удалена"}