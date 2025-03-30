"""
Модели для социального модуля
"""

from sqlmodel import Field, Relationship
from pydantic import EmailStr

from core.models import BaseModel, DomainModel

class UserGroupLink(BaseModel, table=True):
    """
    Связь пользователей с группами
    """

    __tablename__ = "user_group_link"

    user_id: int = Field(foreign_key="user.id", primary_key=True)
    group_id: int = Field(foreign_key="group.id", primary_key=True)


class UserBase(BaseModel):
    """
    Базовая модель пользователя
    """

    username: str
    password: str
    steam_username: str | None
    first_name: str | None
    last_name: str | None
    email: EmailStr | None


class User(UserBase, table=True):
    """
    Модель пользователя
    """

    __tablename__ = "user"

    groups: list["Group"] = Relationship(back_populates="users", link_model=UserGroupLink)


class GroupBase(DomainModel):
    """
    Базовая модель группы
    """

    name: str


class Group(GroupBase, table=True):
    """
    Модель группы
    """

    __tablename__ = "group"

    users: list[User] = Relationship(back_populates="groups", link_model=UserGroupLink)

