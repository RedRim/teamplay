from typing import Any, Union, Annotated
from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends,
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer
from sqlmodel import select

from .schemas import (
    TokenInfo,
    RegisterUserSchema,
)
from core.models import async_session_maker
from .models import (
    UserBase,
    User,
) 
from .utils import (
   hash_password, 
   validate_password,
   create_access_token,
   create_refresh_token, 
)
from .validation import (
    get_current_token_payload,
    get_current_auth_user,
)


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix="/auth",
    tags=["auth"], 
    dependencies=[Depends(http_bearer)],
)

security = HTTPBasic()

@router.post("/register")
async def register_user(data: RegisterUserSchema):
    async with async_session_maker() as session:
        query = select(User).where(User.username == data.username)
        result = await session.exec(query)
        check_user_instance = result.one_or_none()
        if check_user_instance is not None:
            raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
        
        data.password = hash_password(data.password)
        user = User(**data.model_dump())
        session.add_all(user)
        await session.commit()

        return user
    

@router.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    async with async_session_maker() as session:
        query = select(User).where(User.username == credentials.username)
        result = await session.exec(query)
        user_instance = result.one_or_none()
        if user_instance is None:
            raise HTTPException(status_code=400, detail="Пользователь не найден")
        
        if not validate_password(credentials.password, user_instance.password):
            raise HTTPException(status_code=400, detail="Неверный пароль")

        access_token = create_access_token(user_instance)
        refresh_token = create_refresh_token(user_instance)
    
        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    
@router.get("/me")
async def get_user_info(
    payload: dict = Depends(get_current_token_payload),
    user: User = Depends(get_current_auth_user),
):
    iat = payload.get("iat")
    return payload


@router.post("/users/create", response_model=User)
async def create_user  (data: UserBase):
    async with async_session_maker() as session:
        user = User(**data.model_dump())
        session.add(user)
        await session.commit()

        return user


@router.get("/users", response_model=list[UserBase])
async def get_user():
    async with async_session_maker() as session:
        query = select(User)
        results = await session.exec(query)
        instances = results.all()

        return instances
    

@router.get("/users/{id}", response_model=Union[User, None])
async def get_user(id: int):
    model = User
    async with async_session_maker() as session:
        query = select(model).where(model.id == id)
        result = await session.exec(query)
        instance = result.one_or_none()
        if instance is None:
            raise HTTPException(status_code=404, detail=f"Не найдено записи в таблице {model.__name__} с {id=}")

        return instance


@router.patch("/users/{id}", response_model=Union[User, None])
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
    
@router.delete("/users/{id}", response_model=dict)
async def delete_user(id: int):
    model = User
    async with async_session_maker() as session:
        query = select(model).where(model.id == id)
        result = await session.exec(query)
        instance = result.one_or_none()
        if instance is None:
            raise HTTPException(status_code=404, detail=f"Не найдено записи в таблице {model.__name__} c {id=}")
        await session.delete(instance)
        await session.commit()

        return {"success": f"Запись {model.__name__} c {id=} удалена"}