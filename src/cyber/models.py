"""
Модели для модуля киберспорта
"""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import DateTime, func

from core.models import BaseModel, DomainModel

if TYPE_CHECKING:
    from auth.models import User


class GameBase(BaseModel):
    """
    Базовая модель игры
    """

    title: str
    photo_path: str | None = None


class Game(GameBase, table=True):
    """
    Игра
    """

    __tablename__ = "game"


class EventUsersCnt(int, Enum):
    """
    Максимальное количество команд
    """

    ONE = 1
    TWO = 2
    FOUR = 4
    EIGHT = 8
    SIXTEEN = 16
    THIRTY_TWO = 32
    SIXTY_FOUR = 64


class TeamPlayersCnt(int, Enum):
    """
    Тип команды (количество игроков в команде)
    """

    ONE = 1
    TWO = 2
    FIVE = 5


class EventBase(BaseModel):
    """
    Базовая модель мероприятия
    """

    title: str
    max_players: EventUsersCnt | None = Field(default=EventUsersCnt.SIXTY_FOUR)
    team_type: TeamPlayersCnt | None = Field(default=TeamPlayersCnt.ONE)
    date_from: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
    )
    date_to: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
    )
    organizer_id: int | None = Field(foreign_key="user.id", default=None)
    game_id: int | None = Field(foreign_key="game.id", default=None)


class TeamEventLink(SQLModel, table=True):
    """
    Связь команд с мероприятиями
    """

    __tablename__ = "team_event_link"

    team_id: int = Field(foreign_key="team.id", primary_key=True)
    event_id: int = Field(foreign_key="event.id", primary_key=True)


class Event(EventBase, table=True):
    """
    Мероприятие
    """

    __tablename__ = "event"

    organizer: Optional["User"] = Relationship(back_populates="created_events")
    game: Game | None = Relationship()
    teams: list["Team"] = Relationship(back_populates='events', link_model=TeamEventLink)


class TeamBase(BaseModel):
    """
    Базовая модель команды
    """

    name: str
    players_cnt: TeamPlayersCnt | None = Field(default=TeamPlayersCnt.FIVE)
    captain_id: int = Field(foreign_key="user.id", default=None)


class TeamUserLink(SQLModel, table=True):
    """
    Связь команд с пользователями
    """

    __tablename__ = "team_user_link"

    team_id: int = Field(foreign_key="team.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)


class Team(TeamBase, table=True):
    """
    Модель команды
    """

    __tablename__ = "team"

    users: list["User"] = Relationship(back_populates="teams", link_model=TeamUserLink)
    events: list[Event] = Relationship(back_populates="teams", link_model=TeamEventLink)
    captain: "User" = Relationship()

    

