from sqlmodel import Field, Relationship, SQLModel

class TeamUserRequest(SQLModel, table=True):
    """
    Запрос на приглашение пользователя в команду
    """

    __tablename__ = "team_user_request"

    team_id: int = Field(foreign_key="team.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)


class FriendshipRequest(SQLModel, table=True):
    """
    Запрос на добавление друга
    """

    __tablename__ = "friendship_request"

    user_from_id: int = Field(foreign_key="user.id", primary_key=True)
    user_to_id: int = Field(foreign_key="user.id", primary_key=True)