from fastapi import Depends, HTTPException, status, Form
from jwt.exceptions import InvalidTokenError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer

from auth.schemas import UserSchema
from .helpers import (
    TOKEN_TYPE_FIELD, 
    ACCESS_TOKEN_TYPE, 
    REFRESH_TOKEN_TYPE,
)
from core import utils as auth_utils 
from .crud import users_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/jwt/login')



def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    """
    для получения нагрузки по юзеру
    """
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload

def validate_token_type(
        payload: dict,
        token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if payload.get(TOKEN_TYPE_FIELD) == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'invalid token type {current_token_type!r} expected {token_type!r}'
    )

def get_user_by_token_sub(payload: dict) -> UserSchema:
    '''
    возвращает юзера по имени
    '''
    username: str | None = payload.get('sub')
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )
    

def get_auth_user_from_token_of_type(token_type: str):
    def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload),
    ) -> UserSchema:
        validate_token_type(payload, token_type)
        return get_user_by_token_sub(payload)

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

get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE) # чтобы обновить токен

def get_current_active_auth_user( # me
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )

def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid username or password'
    )

    if not (user := users_db.get(username)):
        raise unauthed_exc
    
    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password
    ):
        raise unauthed_exc
    
    return user
