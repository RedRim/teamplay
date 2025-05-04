"""
Модели для социального модуля
"""

from sqlmodel import Field, Relationship, CheckConstraint, UniqueConstraint
from pydantic import EmailStr

from enum import Enum

from core.models import BaseModel, DomainModel
from cyber.models import Event, Team, TeamUserLink

class UserGroupLink(BaseModel, table=True):
    """
    Связь пользователей с группами
    """

    __tablename__ = "user_group_link"

    user_id: int = Field(foreign_key="user.id", primary_key=True)
    group_id: int = Field(foreign_key="group.id", primary_key=True)


class UserType(int, Enum):
    """
    Тип пользователя
    """

    USER = 0
    PRO = 1
    MANAGER = 2
    ADMIN = 3

class UserBase(BaseModel):
    """
    Базовая модель пользователя
    """

    username: str | None = None
    password: str | None = None
    steam_username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    age: int | None = None
    city: str | None = None
    country: str | None = None
    user_type: UserType | None = Field(default=UserType.USER)


class User(UserBase, table=True):
    """
    Модель пользователя
    """

    __tablename__ = "user"

    groups: list["Group"] = Relationship(back_populates="users", link_model=UserGroupLink)
    posts: list["Post"] = Relationship(back_populates="created_by")
    created_events: list[Event] = Relationship(back_populates="organizer")
    teams: list[Team] = Relationship(back_populates="users", link_model=TeamUserLink)


class FriendsLink(BaseModel, table=True):
    """
    Модель связи друзей
    """

    __tablename__ = "friendslink"

    user_id: int | None = Field(foreign_key="user.id", default=None, primary_key=True)
    friend_id: int | None = Field(foreign_key="user.id", default=None, primary_key=True)

    __table_args__ = (
        CheckConstraint("user_id != friend_id", name="check_not_self_friendship"),
        UniqueConstraint("user_id", "friend_id", name="unique_user_pair_friendship"),
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
    posts: list["Post"] = Relationship(back_populates="group")


class PostBase(DomainModel):
    """
    Базовая модель постов
    """

    text: str | None = None
    photo_path: str | None = None

    group_id: int | None = Field(foreign_key="group.id", default=None)
    # team_id: int | None = Field(foreign_key="team.id", default=None) TODO


class Post(PostBase, table=True):
    """
    Модель постов
    """

    created_by: User | None = Relationship(back_populates="posts")
    group: Group | None = Relationship(back_populates="posts")
    # team: Team | None = Relationship(back_populates="posts")