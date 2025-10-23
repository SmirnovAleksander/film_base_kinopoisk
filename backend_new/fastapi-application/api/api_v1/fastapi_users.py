import uuid

from fastapi_users import FastAPIUsers

from core.models import User
from core.types.user_id import UserIdType
from api.dependencies.authentification.user_manager import get_user_manager
from api.dependencies.authentification.backend import auth_backend

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [auth_backend],
)