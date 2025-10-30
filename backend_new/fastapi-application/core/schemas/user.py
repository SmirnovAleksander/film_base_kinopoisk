from typing import Optional
from fastapi_users import schemas

from core.types.user_id import UserIdType


class UserRead(schemas.BaseUser[UserIdType]):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(schemas.BaseUserCreate):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None