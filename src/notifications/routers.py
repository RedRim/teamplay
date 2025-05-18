from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends,
    status,
)

from fastapi.security import HTTPBearer
from sqlmodel import select

from auth.validation import get_current_auth_user
from auth.models import User, FriendsLink
from cyber.models import Team, TeamUserLink
from core.models import async_session_maker
from core.utils import get_object_or_404
from notifications.models import TeamUserRequest, FriendshipRequest


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix="/notifications",
    tags=["notifications"], 
    dependencies=[Depends(http_bearer)],
)

@router.post("/friendship_requests/create")
async def friendship_request_create(
    user_to_id: int,
    user: User = Depends(get_current_auth_user),
):
    """
    Создать запрос на дружбу
    """
    async with async_session_maker() as session:
        friendship_request = FriendshipRequest(user_from_id=user.id, user_to_id=user_to_id)
        session.add(friendship_request)
        await session.commit()

        return friendship_request

@router.get("/friendship_requests/incoming", response_model=list[FriendshipRequest])
async def get_incoming_friendship_requests(user: User = Depends(get_current_auth_user),):
    """
    Список входящих запросов на дружбу
    """
    async with async_session_maker() as session:
        query = select(FriendshipRequest).where(FriendshipRequest.user_to_id==user.id)
        results = await session.exec(query)
        instances = results.all()

        return instances

@router.get("/friendship_requests/outgoing", response_model=list[FriendshipRequest])
async def get_outgoing_friendship_requests(user: User = Depends(get_current_auth_user),):
    """
    Список исходящих запросов на дружбу
    """
    async with async_session_maker() as session:
        query = select(FriendshipRequest).where(FriendshipRequest.user_from_id==user.id)
        results = await session.exec(query)
        instances = results.all()

        return instances
    
@router.post("/friendship_requests/accept")
async def friendship_request_accept(
    data: FriendshipRequest,
    user: User = Depends(get_current_auth_user),
):
    """
    Принятие запроса на дружбу
    """
    async with async_session_maker() as session:
        query = select(FriendshipRequest).where(
            FriendshipRequest.user_from_id==data.user_from_id,
            FriendshipRequest.user_to_id==data.user_to_id,
        )
        result = await session.exec(query)
        request = result.one_or_none()
        if request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Записи {request.__class__.__name__} с {id=} не найдено"
            )
        session.add_all([
            FriendsLink(user_id=user.id, friend_id=request.user_from_id),
            FriendsLink(user_id=request.user_from_id, friend_id=user.id)
        ])
        await session.delete(request)
        await session.commit()

        return {"status": "success"}

@router.post("/friendship_requests/decline")
async def friendship_request_decline(
    data: FriendshipRequest,
    user: User = Depends(get_current_auth_user),
):
    """
    Отклонение запроса на дружбу
    """
    async with async_session_maker() as session:
        query = select(FriendshipRequest).where(
            FriendshipRequest.user_from_id==data.user_from_id,
            FriendshipRequest.user_to_id==data.user_to_id,
        )
        result = await session.exec(query)
        request = result.one_or_none()
        if request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Записи {request.__class__.__name__} с {id=} не найдено"
            )
        session.delete(request)
        session.commit()

        return {"status": "success"}
    

@router.post("/team_user_requests/create/")
async def team_user_requests_create(
    data: TeamUserRequest,
    user: User = Depends(get_current_auth_user),
):
    """
    Создать запрос на приглашение в команду
    """
    async with async_session_maker() as session:
        team = get_object_or_404(Team, data.team_id, session)
        get_object_or_404(User, data.user_id, session)
        if user.id != team.captain_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Приглашать в команду может только капитан"
            )

        team_user_request = TeamUserRequest(**data.model_dump())
        session.add(team_user_request)
        await session.commit()

        return team_user_request

@router.get("/team_user_requests", response_model=list[TeamUserRequest])
async def get_team_user_requests():
    """
    Список запросов на приглашение в команду
    """
    async with async_session_maker() as session:
        query = select(TeamUserRequest)
        results = await session.exec(query)
        instances = results.all()

        return instances

@router.post("/team_user_requests/accept")
async def team_user_request_accept(
    request_id: int,
    user: User = Depends(get_current_auth_user),
):
    """
    Принятие запроса на приглашение в команду
    """
    async with async_session_maker() as session:
        request = get_object_or_404(TeamUserRequest, request_id, session)
        session.add(TeamUserLink(user_id=user.id, team_id=request.team_id))
        session.delete(request)
        session.commit()

        return {"status": "success"}

@router.post("/team_user_requests/decline")
async def team_user_request_decline(
    request_id: int,
    user: User = Depends(get_current_auth_user),
):
    """
    Отклонение запроса на приглашение в команду
    """
    async with async_session_maker() as session:
        request = get_object_or_404(TeamUserRequest, request_id, session)
        session.delete(request)
        session.commit()

        return {"status": "success"}