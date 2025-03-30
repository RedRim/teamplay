from sqlmodel import SQLModel, Field
from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from datetime import datetime
from .config import setup_config

DATABASE_URL = setup_config().db.dsn
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class BaseModel(SQLModel):
    """
    Базовая модель
    """

    id: int = Field(primary_key=True)


class RoleUserModel(BaseModel):
    """
    Поля пользователя создавшего модель
    """

    created_by_id: int | None = Field(foreign_key="user.id")


class TimestampedModel(BaseModel):
    """
    Поля пользователя создавшего модель
    """

    created_datetime: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
    )
    updated_datetime: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"onupdate": datetime.now, "server_default": func.now()},
    )


class DomainModel(RoleUserModel, TimestampedModel):
    """
    Общие поля для объектов доменной модели
    """
