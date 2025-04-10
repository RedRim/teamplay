import time
from typing import Any, Union, Annotated
import secrets
import uuid
from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends, 
    status, 
    Header,
    Response,
    Cookie,
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from core.models import async_session_maker
from .models import (
    UserBase,
    User,
    Profile,
) 
from sqlmodel import select

router = APIRouter(prefix="/auth", tags=["auth"])

security = HTTPBasic()

@router.get("/basic-auth")
async def demo_basic_auth(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "message": "Hi!",
        "username": credentials.username,
        "password": credentials.password,
    }


username_to_passwords = {
    "admin": "admin",
    "john": 'password',
}

static_auth_token_to_username = {
    "4a38a65d796c8ab7ad136887a2e3d": "admin",
    "be4261f06080571c469c71628b83d": 'john',
}


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = username_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc
    
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8")
    ):
        raise unauthed_exc
    
    return credentials.username

def get_username_by_static_auth_token(
        static_token: str = Header(alias="x-auth-token")
) -> str:
    if username := static_auth_token_to_username.get(static_token):
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invaid"
    )
    

@router.get("/basic-auth-username")
async def demo_auth(
    auth_username: str = Depends(get_auth_user_username)
):
    
    return {
        "message": f"Hi, {auth_username}!"
    }

@router.get("/some-http-header-auth")
async def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token)
):
    
    return {
        "message": f"Hi, {username}!"
    }

COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"

def generate_sesssion_id() -> str:
    return uuid.uuid4().hex


@router.post("/login-cookie")
async def demo_auth_login_cookie(
    response: Response,
    # username: str = Depends(get_auth_user_username),
    username: str = Depends(get_username_by_static_auth_token),
):
    session_id = generate_sesssion_id()
    COOKIES[session_id] = {
        'username': username,
        'login_at': int(time.time())
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {
        "result": "OK"
    }


def get_session_data(
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
):
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='not authenticated',
        )
    
    return COOKIES[session_id]


@router.get('/check-cookie')
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data)
):
    username = user_session_data["username"]
    return {
        'message': f'hello, {username}',
        **user_session_data,
    }


@router.get('/logout-cookie')
def demo_auth_logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {
        'message': f'bye, {username}',
    }











@router.post("/users/create", response_model=User)
async def create_user  (data: UserBase):
    async with async_session_maker() as session:
        print(data.model_dump())
        user = User(**data.model_dump())
        profile = Profile(user=user)
        session.add(user)
        session.add(profile)
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
        profile_query = select(Profile).where(Profile.user_id==instance.id)
        profile = await session.exec(profile_query)
        profile_instance = profile.one_or_none()
        if profile_instance:
            await session.delete(profile_instance)
        await session.delete(instance)
        await session.commit()

        return {"success": f"Запись {model.__name__} c {id=} удалена"}