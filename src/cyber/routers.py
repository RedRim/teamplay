from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends,
)

from fastapi.security import HTTPBearer

from auth.validation import (
    get_current_auth_user,
)
from auth.models import User
from cyber.models import Event
from core.models import async_session_maker


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix="/cyber",
    tags=["cyber"], 
    dependencies=[Depends(http_bearer)],
)

@router.post("/new_event")
async def get_user_info(
    user: User = Depends(get_current_auth_user),
):
    async with async_session_maker() as session:
        event = Event(organizer=user, title='Major')
        session.add(event)
        await session.commit()

        return event
    
