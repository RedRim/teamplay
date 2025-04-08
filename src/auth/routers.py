from fastapi import APIRouter, HTTPException

from src.core.models import async_session_maker
from .models import UserBase, User
from .test_models import Hero, Team
from sqlmodel import select

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/heroes", response_model=list[Hero])
async def get_heroes():
    async with async_session_maker() as session:
        query = select(Hero)
        results = await session.exec(query)
        instances = results.all()
        print('hero')
        return instances
    
@auth_router.post("/heroes/create", response_model=Hero)
async def create_hero(data: Hero):
    async with async_session_maker() as session:
        print(data.model_dump())
        hero = Hero(**data.model_dump())
        # profile = Profile()
        session.add(hero)
        print('user before commit')
        print(hero)
        await session.commit()
        print('user after commit')
        print(hero)
        await session.refresh(hero)
        print('user after refresh')
        print(hero)

        return hero
    


@auth_router.post("/user/create", response_model=User)
async def create_user(data: UserBase):
    async with async_session_maker() as session:
        print(data.model_dump())
        user = User(**data.model_dump())
        # profile = Profile()
        session.add(user)
        print('user before commit')
        print(user)
        await session.commit()
        print('user after commit')
        print(user)
        await session.refresh(user)
        print('user after refresh')
        print(user)

        return user


@auth_router.get("/user", response_model=list[UserBase])
async def get_user():
    async with async_session_maker() as session:
        query = select(User)
        results = await session.exec(query)
        instances = results.all()

        return instances
    

@auth_router.get("/user/{id}", response_model=User)
async def get_user(id: int):
    model = User
    async with async_session_maker() as session:
        query = select(model).where(model.id == id)
        result = await session.exec(query)
        instance = result.one()

        return instance


@auth_router.patch("/user/{id}", response_model=User)
async def update_user(id: int, data: UserBase):
    model = User
    async with async_session_maker() as session:
        query = select(model).where(model.id == id)
        result = await session.exec(query)
        instance = result.one_or_none()
        if instance is None:
            raise HTTPException(f"Не найдено записи в таблице {model.__class__.__name__} с {id=}")
        test = data.model_dump(exclude_unset=False)
        test_2 = data.model_dump(exclude_unset=True)
        print(test)
        print(test_2)

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, key, value)
        
        session.add(instance)
        session.commit()
        session.refresh()

        return instance
    
@auth_router.delete("user/{id}", response_model=dict)
async def delete_user(id: int):
    model = User
    async with async_session_maker() as session:
        query = select(model).where(model.id == id)
        result = await session.exec(query)
        instance = result.one_or_none()
        if instance is None:
            raise HTTPException(f"Не найдено записи в таблице {model.__class__.__name__} c {id=}")
        
        await session.delete(instance)
        await session.commit()

        return {"success": f"Запись {model.__class__.__name__} c {id=} удалена"}