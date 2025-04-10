from datetime import timedelta, datetime
import uuid
import jwt

import bcrypt

from .config import setup_config

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
    return bcrypt.hashpw(pwd_bytes, salt)

def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password
    )