from fastapi import Depends, HTTPException, status, Form
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select

from auth.schemas import UserSchema
from .models import User

from .utils import decode_jwt, validate_password
from core.config import setup_config
from core.models import async_session_maker

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')
auth_jwt = setup_config().auth_jwt


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Токен недейсвителен: {e}",
        )
    return payload

async def validate_token_type(
        payload: dict,
        token_type: str,
) -> str:
    current_token_type = payload.get(auth_jwt.TOKEN_TYPE_FIELD)
    if payload.get(auth_jwt.TOKEN_TYPE_FIELD) == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'Неверный тип токена {current_token_type!r}. Ожидалось: {token_type!r}'
    )

async def get_user_by_token_sub(payload: dict) -> User:
    user_id: int | None = payload.get('id')
    async with async_session_maker() as session:
        query = select(User).where(User.id == user_id)
        result = await session.exec(query)
        user_instance = result.one_or_none()
        if user_instance is not None:
            return user_instance

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Токен невалиден или пользователь не найден",
    )
    

def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload),
    ) -> UserSchema:
        await validate_token_type(payload, token_type)
        return await get_user_by_token_sub(payload)

    return get_auth_user_from_token

class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
    ):
        validate_token_type(payload, self.token_type)
        return get_user_by_token_sub(payload)

get_current_auth_user = get_auth_user_from_token_of_type(auth_jwt.ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(auth_jwt.REFRESH_TOKEN_TYPE)

async def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Пользователь нективен",
    )

async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Неверное имя пользователя или пароль'
    )
    async with async_session_maker() as session:
        query = select(User).where(User.username == username)
        result = await session.exec(query)
        user_instance = result.one_or_none()
        
    if user_instance is None:
        raise unauthed_exc
    
    if not validate_password(
        password=password,
        hashed_password=user_instance.password
    ):
        raise unauthed_exc
    
    return user_instance
