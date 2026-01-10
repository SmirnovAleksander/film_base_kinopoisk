from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, SimilarContent
from core.schemas import (
    SimilarContentRead,
    SimilarContentCreate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/similar-content",
    dependencies=[Depends(current_active_superuser)],
)


# POST /api/v1/admin/similar-content - Создать вручную связь между двумя похожими фильмами или сериалами
@router.post("", response_model=SimilarContentRead, summary="Создать связь похожего контента")
async def create_similar_content_admin(
    similar_data: SimilarContentCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать связь похожего контента (только для суперпользователя)"""
    dup_stmt = select(SimilarContent).where(
        SimilarContent.content_id == similar_data.content_id,
        SimilarContent.content_type == similar_data.content_type,
        SimilarContent.similar_id == similar_data.similar_id,
    )
    dup_result = await session.execute(dup_stmt)
    duplicate = dup_result.scalar_one_or_none()
    if duplicate:
        raise HTTPException(status_code=400, detail="Similar content association already exists")

    similar = SimilarContent(**similar_data.model_dump(exclude_unset=True))
    session.add(similar)
    await session.commit()
    await session.refresh(similar)

    return SimilarContentRead.model_validate(similar)


# GET /api/v1/admin/similar-content?content_id=1 - Получить список всех рекомендаций для конкретного ID
@router.get("", response_model=list[SimilarContentRead], summary="Список похожего контента")
async def list_similar_content_admin(
    content_id: int | None = Query(None, description="ID контента"),
    content_type: str | None = Query(None, description="Тип контента (film/series)"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список всех похожих связей (только для суперпользователя)"""
    stmt = select(SimilarContent).order_by(SimilarContent.id.desc())
    
    conditions = []
    if content_id is not None:
        conditions.append(SimilarContent.content_id == content_id)
    if content_type is not None:
        conditions.append(SimilarContent.content_type == content_type)
        
    if conditions:
        stmt = stmt.where(and_(*conditions))

    result = await session.execute(stmt)
    similar_list = result.scalars().all()

    return [SimilarContentRead.model_validate(item) for item in similar_list]


# GET /api/v1/admin/similar-content/1 - Получить детали конкретной записи о похожести
@router.get("/{similar_id_pk}", response_model=SimilarContentRead, summary="Детали похожего контента")
async def get_similar_content_admin(
    similar_id_pk: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали связи похожего контента по ID (только для суперпользователя)"""
    stmt = select(SimilarContent).where(SimilarContent.id == similar_id_pk)
    result = await session.execute(stmt)
    similar = result.scalar_one_or_none()

    if not similar:
        raise HTTPException(status_code=404, detail="Similar content association not found")

    return SimilarContentRead.model_validate(similar)


# DELETE /api/v1/admin/similar-content/1 - Удалить запись о похожести контента из базы
@router.delete("/{similar_id_pk}", response_model=OperationResponse, summary="Удалить похожий контент")
async def delete_similar_content_admin(
    similar_id_pk: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить связь похожего контента (только для суперпользователя)"""
    stmt = select(SimilarContent).where(SimilarContent.id == similar_id_pk)
    result = await session.execute(stmt)
    similar = result.scalar_one_or_none()

    if not similar:
        raise HTTPException(status_code=404, detail="Similar content association not found")

    await session.delete(similar)
    await session.commit()

    return OperationResponse(
        status="success",
        message="Similar content association deleted successfully",
        id=similar_id_pk,
    )
