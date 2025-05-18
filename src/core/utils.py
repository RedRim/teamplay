from datetime import timedelta, datetime
import uuid
import jwt
from fastapi import HTTPException,  status
from sqlmodel import select
from core.models import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
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
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8') 


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode('utf-8') 
    )

async def get_object_or_404(model: type[BaseModel], id: int, session: AsyncSession) -> BaseModel:
    """
    Получение записи по id
    Если не найдено - бросает 404
    """

    query = select(model).where(model.id==id)
    result = await session.exec(query)
    instance = result.one_or_none()
    if instance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Записи {model.__name__} с {id=} не найдено"
        )
    return instance