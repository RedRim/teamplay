"""
Модели для социального модуля
"""

from sqlmodel import Field, Relationship, CheckConstraint, UniqueConstraint
from pydantic import EmailStr

from enum import Enum
from typing import Optional

from src.core.models import BaseModel, DomainModel

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

    profile_id: int | None = Field(default=None, foreign_key="profile.id")


class User(UserBase, table=True):
    """
    Модель пользователя
    """

    __tablename__ = "user"

    profile: Optional["Profile"] = Relationship(back_populates="user")
    groups: list["Group"] = Relationship(back_populates="users", link_model=UserGroupLink)


class UserType(int, Enum):
    """
    Тип пользователя
    """

    USER = 0
    PRO = 1
    MANAGER = 2
    ADMIN = 3


class FriendsLink(BaseModel, table=True):
    """
    Модель связи друзей
    """

    __tablename__ = "friendslink"

    user_1_id: int = Field(foreign_key="profile.id", default=None, primary_key=True)
    user_2_id: int = Field(foreign_key="profile.id", default=None, primary_key=True)

    __table_args__ = (
        CheckConstraint("user_1_id != user_2_id", name="check_not_self_freindship"),
        UniqueConstraint("user_1_id", "user_2_id", name="unique_user_pair_freindship"),
        UniqueConstraint("user_2_id", "user_1_id", name="unique_user_pair_freindship_reverse")
    )


class ProfileBase(BaseModel):
    """
    Базовая модель профиля
    """

    age: int | None
    city: str | None
    country: str | None
    user_type: UserType | None = Field(default=UserType.USER)

    user_id: int | None = Field(foreign_key="user.id", default=None)


class Profile(ProfileBase, table=True):
    """
    Модель профиля
    """

    __tablename__ = "profile"

    user: User = Relationship(
        sa_relationship_kwargs={"uselist": False},
        back_populates="profile"
    )
    friends: list["Profile"] = Relationship(
        back_populates="friends",
        link_model=FriendsLink
    )


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

