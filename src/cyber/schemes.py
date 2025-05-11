from pydantic import BaseModel

class TeamUserLinkScheme(BaseModel):
    """
    Схема для добавления юзеров в команду
    """

    team_id: int
    user_ids: list[int]


class EventTeamLinkScheme(BaseModel):
    """
    Схема для добавления команды на турнир
    """

    event_id: int
    team_id: int
