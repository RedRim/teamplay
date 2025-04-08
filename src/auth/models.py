"""
Модели для социального модуля
"""

from sqlmodel import Field, Relationship, CheckConstraint, UniqueConstraint
from pydantic import EmailStr

from enum import Enum
from typing import Optional

from src.core.models import BaseModel, DomainModel

# class UserGroupLink(BaseModel, table=True):
#     """
#     Связь пользователей с группами
#     """

#     __tablename__ = "user_group_link"

#     user_id: int = Field(foreign_key="user.id", primary_key=True)
#     group_id: int = Field(foreign_key="group.id", primary_key=True)


class UserBase(BaseModel):
    """
    Базовая модель пользователя
    """

    username: str
    password: str
    steam_username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class User(UserBase, table=True):
    """
    Модель пользователя
    """

    __tablename__ = "uuser"

    username: str
    password: str
    steam_username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None

    # groups: list["Group"] = Relationship(back_populates="users", link_model=UserGroupLink)
    # profile: "Profile" = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})
    posts: list["Post"] = Relationship(back_populates="author")


# class UserType(int, Enum):
#     """
#     Тип пользователя
#     """

#     USER = 0
#     PRO = 1
#     MANAGER = 2
#     ADMIN = 3



# class FriendsLink(BaseModel, table=True):
#     """
#     Модель связи друзей
#     """

#     __tablename__ = "friendslink"

#     user_id: int | None = Field(foreign_key="user.id", default=None, primary_key=True)
#     friend_id: int | None = Field(foreign_key="user.id", default=None, primary_key=True)

#     __table_args__ = (
#         CheckConstraint("user_id != friend_id", name="check_not_self_friendship"),
#         UniqueConstraint("user_id", "friend_id", name="unique_user_pair_friendship"),
#         UniqueConstraint("friend_id", "user_id", name="unique_user_pair_friendship_reverse")
#     )


# class ProfileBase(BaseModel):
#     """
#     Базовая модель профиля
#     """

#     age: int | None = None
#     city: str | None = None
#     country: str | None = None
#     user_type: UserType | None = Field(default=UserType.USER)

#     user_id: int | None = Field(foreign_key="user.id", default=None)


# class Profile(ProfileBase, table=True):
#     """
#     Модель профиля
#     """

#     __tablename__ = "profile"

#     user: User = Relationship(
#         back_populates="profile",
#         sa_relationship_kwargs={"uselist": False},
#     )


# class GroupBase(DomainModel):
#     """
#     Базовая модель группы
#     """

#     name: str


# class Group(GroupBase, table=True):
#     """
#     Модель группы
#     """

#     __tablename__ = "group"

#     users: list[User] = Relationship(back_populates="groups", link_model=UserGroupLink)

class PostBase(DomainModel):
    """
    Базовая модель постов
    """

    text: str | None = None
    photo_path: str | None = None

    # group_id: int | None = Field(foreign_key="group.id", default=None)
    # team_id: int | None = Field(foreign_key="team.id", default=None) TODO


class Post(PostBase, table=True):
    """
    Модель постов
    """

    created_by: User | None = Relationship(back_populates="posts")
    # group: Group | None = Relationship(back_populates="posts")
    # team: Team | None = Relationship(back_populates="posts")