from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from core.models import db_helper, User
from core.schemas import (
    UserRead,
    UserCreate,
    UserUpdate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser
from core.authentication.user_manager import UserManager

router = APIRouter(
    prefix="/users",
    dependencies=[Depends(current_active_superuser)],
)


@router.post("", response_model=UserRead, summary="Создать пользователя")
async def create_user_admin(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать нового пользователя (только для суперпользователя)"""
    users_db = User.get_db(session)
    user_manager = UserManager(users_db, background_tasks=background_tasks)
    
    try:
        user = await user_manager.create(
            user_create=user_data,
            safe=False  # Разрешаем устанавливать is_superuser и is_verified
        )
        await session.refresh(user)
        return UserRead.model_validate(user)
    except ValueError as e:
        error_msg = str(e).lower()
        if "email" in error_msg or "username" in error_msg:
            raise HTTPException(status_code=400, detail="User with this email or username already exists")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await session.rollback()
        error_msg = str(e).lower()
        if "email" in error_msg or "username" in error_msg or "unique" in error_msg:
            raise HTTPException(status_code=400, detail="User with this email or username already exists")
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")


@router.get("", response_model=list[UserRead], summary="Список пользователей")
async def list_users_admin(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(50, ge=1, le=100, description="Размер страницы"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список всех пользователей с пагинацией (только для суперпользователя)"""
    offset = (page - 1) * page_size

    stmt = (
        select(User)
        .order_by(User.id)
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    users = result.scalars().all()

    return [UserRead.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserRead, summary="Детали пользователя")
async def get_user_admin(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали пользователя по ID (только для суперпользователя)"""
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead.model_validate(user)


@router.put("/{user_id}", response_model=UserRead, summary="Обновить пользователя")
async def update_user_admin(
    user_id: int,
    user_data: UserUpdate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Обновить пользователя (только для суперпользователя)"""
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    users_db = User.get_db(session)
    user_manager = UserManager(users_db, background_tasks=background_tasks)
    
    try:
        updated_user = await user_manager.update(
            user_update=user_data,
            user=user,
            safe=False  # Разрешаем изменять is_superuser и is_verified
        )
        await session.refresh(updated_user)
        return UserRead.model_validate(updated_user)
    except ValueError as e:
        error_msg = str(e).lower()
        if "email" in error_msg or "username" in error_msg:
            raise HTTPException(status_code=400, detail="User with this email or username already exists")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await session.rollback()
        error_msg = str(e).lower()
        if "email" in error_msg or "username" in error_msg or "unique" in error_msg:
            raise HTTPException(status_code=400, detail="User with this email or username already exists")
        raise HTTPException(status_code=400, detail=f"Error updating user: {str(e)}")


@router.delete("/{user_id}", response_model=OperationResponse, summary="Удалить пользователя")
async def delete_user_admin(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить пользователя (только для суперпользователя)"""
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()

    return OperationResponse(
        status="success",
        message="User deleted successfully",
        id=user_id
    )

