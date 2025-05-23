from auth.schemas import UserSchema
from core import utils as auth_utils 
from core.config import setup_config

from datetime import timedelta

TOKEN_TYPE_FIELD = 'type'
ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'
auth_jwt = setup_config().auth_jwt

def create_jwt(
        token_type :str, 
        token_data: dict,
        expire_minutes: int = auth_jwt.access_token_expire,
        expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return auth_utils.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta
)

def create_access_token(user: UserSchema) -> str:
    jwt_payload = {
        'sub': user.username,
        'username': user.username, 
        'email': user.email,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE, 
        token_data=jwt_payload,
        expire_minutes=auth_jwt.access_token_expire,
    )


def create_refresh_token(user: UserSchema) -> str:
    jwt_payload = {
        'sub': user.username
       }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE, 
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=auth_jwt.refresh_token_expire_days)
    )
