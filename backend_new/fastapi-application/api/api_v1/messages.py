from fastapi import APIRouter
from fastapi import Depends

from api.api_v1.fastapi_users import current_active_user, current_active_superuser
from core.config import settings
from core.models import User
from core.schemas.message import MessageResponse

router = APIRouter(
    prefix=settings.api.v1.messages,
    tags=["Messages"],
)

@router.get("", response_model=MessageResponse)
def get_user_messages(
    user: User = Depends(current_active_user)
):
    return MessageResponse(
        messages=["m1", "m2", "m3"],
        user=UserRead.model_validate(user)
    )

@router.get("/secrets", response_model=MessageResponse)
def get_superuser_messages(
    user: User = Depends(current_active_superuser)
):
    return MessageResponse(
        messages=["secret-m1", "secret-m2", "secret-m3"],
        user=UserRead.model_validate(user)
    )