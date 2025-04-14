from datetime import timedelta, datetime
import uuid
import jwt
import bcrypt

from core.config import setup_config

from .models import User

auth_jwt = setup_config().auth_jwt


def encode_jwt(
    payload: dict, 
    private_key = auth_jwt.private_key_path.read_text(), 
    algorithm: str = auth_jwt.algorithm,
    expire_minutes: int = auth_jwt.access_token_expire,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now, jti=str(uuid.uuid4()))
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)

    return encoded


def decode_jwt(
    token: str | bytes, 
    public_key: str = auth_jwt.public_key_path.read_text(), 
    algorithm: str = auth_jwt.algorithm
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    
    return decoded

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

def validate_password(password: str, hashed_password: bytes) -> bool:
    print(f'validate {hashed_password}')
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode('utf-8')
    )

def create_jwt(
        token_type :str, 
        token_data: dict,
        expire_minutes: int = auth_jwt.access_token_expire,
        expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {auth_jwt.TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta
)

def create_access_token(user: User) -> str:
    jwt_payload = {
        'sub': user.username,
        'username': user.username, 
        'email': user.email,
    }
    return create_jwt(
        token_type=auth_jwt.ACCESS_TOKEN_TYPE, 
        token_data=jwt_payload,
        expire_minutes=auth_jwt.access_token_expire,
    )


def create_refresh_token(user: User) -> str:
    jwt_payload = {
        'sub': user.username
    }
    return create_jwt(
        token_type=auth_jwt.REFRESH_TOKEN_TYPE, 
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=auth_jwt.refresh_token_expire_days)
    )
