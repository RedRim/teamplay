from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends,
)

from fastapi.security import HTTPBearer
from sqlmodel import select

from auth.validation import get_current_auth_user

from auth.models import User
from cyber.models import (
  Event, 
  EventBase, 
  Team, 
  TeamBase, 
  TeamUserLink, 
  TeamEventLink, 
)
from core.models import async_session_maker
from core.utils import get_object_or_404
from cyber.schemes import TeamUserLinkScheme, EventTeamLinkScheme
from notifications.models import TeamUserRequest


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix="/cyber",
    tags=["cyber"], 
    dependencies=[Depends(http_bearer)],
)

@router.post("/events/create")
async def create_event(
    data: EventBase,
    user: User = Depends(get_current_auth_user),
):
    """
    Создать турнир
    """
    async with async_session_maker() as session:
        parameters = data.model_dump()
        parameters['organizer_id'] = user.id
        event = Event(**parameters)
        session.add(event)
        await session.commit()

        return event
    

@router.get("/events", response_model=list[Event])
async def get_events():
    """
    Список турниров
    """
    async with async_session_maker() as session:
        query = select(Event)
        results = await session.exec(query)
        instances = results.all()

        return instances
    
@router.post("/events/add_team")
async def add_team_event(
    data: EventTeamLinkScheme,
    user: User = Depends(get_current_auth_user),
):
    """
    Регистрация команды на турнир
    """
    async with async_session_maker() as session:
        team = get_object_or_404(Team, data.team_id, session)
        
        if user.id != team.captain_id:
            raise HTTPException(status_code=404, detail="Зарегистрировать команду может только капитан")
    
        event = get_object_or_404(Event, data.event_id, session)
        team_event_link = TeamEventLink(team_id=team.id, event_id=event.id)
        session.add(team_event_link)
        await session.commit()

        return team_event_link
    

@router.post("/teams/create")
async def create_team(
    data: TeamBase,
    user: User = Depends(get_current_auth_user),
):
    """
    Создать команду
    """
    async with async_session_maker() as session:
        parameters = data.model_dump()
        parameters['captain_id'] = user.id
        team = Team(**parameters)
        session.add(team)
        await session.commit()
        team_user_link = TeamUserLink(user_id=parameters['captain_id'], team_id=team.id)
        session.add(team_user_link)
        await session.commit()

        return team

@router.post("/teams/add_users")
async def add_users_team(
    data: TeamUserLinkScheme,
    user: User = Depends(get_current_auth_user),
):
    """
    Пригласить пользователей в команду TODO
    """
    async with async_session_maker() as session:
        # получение команды
        team = get_object_or_404(Team, data.team_id, session)
        if team.captain_id != user.id:
            raise HTTPException(status_code=404, detail="Новый пользователей может добавлять только капитан")
        
        # добавление пользователей в команду
        new_users = select(User).where(User.id.in_(data.user_ids))
        new_users = await session.exec(new_users)
        new_users = new_users.all()

        # проверка, что именно все введенные id юзеров есть в базе
        existing_user_ids = {user.id for user in new_users}
        for new_user_id in data.user_ids:
            if new_user_id not in existing_user_ids:
                raise HTTPException(status_code=404, detail=f'Пользователь с id={new_user_id} не найден')
        new_link_instances = [
            TeamUserRequest(user_id=new_user_id, team_id=team.id) for new_user_id in existing_user_ids
        ]
        session.add_all(new_link_instances)
        await session.commit()

        return {'success': True}

@router.get("/teams", response_model=list[Team])
async def get_teams():
    """
    Список команд
    """
    async with async_session_maker() as session:
        query = select(Team)
        results = await session.exec(query)
        instances = results.all()

        return instances
    
