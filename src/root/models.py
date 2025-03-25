from sqlmodel import Field as ModelField
from sqlmodel import SQLModel
from sqlalchemy import DateTime, func

from datetime import datetime


class BaseModel(SQLModel):
    """
    Базовая модель
    """

    id: int = ModelField(primary_key=True)


class RoleUserModel(BaseModel):
    """
    Поля пользователя создавшего модель
    """

    created_by_id: int | None = None


class TimestampedModel(BaseModel):
    """
    Поля пользователя создавшего модель
    """

    created_datetime: datetime | None = ModelField(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
    )
    updated_datetime: datetime | None = ModelField(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"onupdate": datetime.now, "server_default": func.now()},
    )


class DomainModel(RoleUserModel, TimestampedModel):
    """
    Общие поля для объектов доменной модели
    """
