from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from ..utils.auth import get_current_user_id, require_admin, require_moderator
from ..utils.db import get_connection


router = APIRouter()


@router.get("/me")
def get_me(user_id: int = Depends(get_current_user_id)):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, email, username, is_email_verified, role, created_at, last_login_at FROM app_user WHERE id=%s", (user_id,))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="User not found")
            return {
                "id": r[0],
                "email": r[1],
                "username": r[2],
                "is_email_verified": r[3],
                "role": r[4],
                "created_at": r[5].isoformat() if r[5] else None,
                "last_login_at": r[6].isoformat() if r[6] else None,
            }
        finally:
            cur.close()


@router.get("/count", summary="Количество всех пользователей")
def get_users_count():
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM app_user")
            count = cur.fetchone()[0]
            return {"count": count}
        finally:
            cur.close()


@router.get("/", summary="Список всех пользователей (только для админов)")
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    role: Optional[str] = Query(None, description="Фильтр по роли"),
    search: Optional[str] = Query(None, description="Поиск по email или username"),
    admin_role: str = Depends(require_admin())
):
    """Получает список всех пользователей с пагинацией и фильтрами"""
    offset = (page - 1) * page_size
    
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Строим запрос с фильтрами
            where_conditions = []
            params = []
            
            if role:
                where_conditions.append("role = %s")
                params.append(role)
            
            if search:
                where_conditions.append("(email ILIKE %s OR username ILIKE %s)")
                params.extend([f"%{search}%", f"%{search}%"])
            
            where_clause = ""
            if where_conditions:
                where_clause = "WHERE " + " AND ".join(where_conditions)
            
            # Получаем пользователей
            cur.execute(
                f"""
                SELECT id, email, username, is_email_verified, role, created_at, last_login_at
                FROM app_user 
                {where_clause}
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """,
                params + [page_size, offset]
            )
            
            rows = cur.fetchall()
            users = []
            for r in rows:
                users.append({
                    "id": r[0],
                    "email": r[1],
                    "username": r[2],
                    "is_email_verified": r[3],
                    "role": r[4],
                    "created_at": r[5].isoformat() if r[5] else None,
                    "last_login_at": r[6].isoformat() if r[6] else None,
                })
            
            # Получаем общее количество
            cur.execute(
                f"""
                SELECT COUNT(*) FROM app_user {where_clause}
                """,
                params
            )
            total_count = cur.fetchone()[0]
            
            return {
                "items": users,
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": (total_count + page_size - 1) // page_size
            }
        finally:
            cur.close()


@router.put("/{user_id}/role", summary="Изменить роль пользователя (только для админов)")
def update_user_role(
    user_id: int,
    new_role: str,
    admin_role: str = Depends(require_admin())
):
    """Изменяет роль пользователя"""
    if new_role not in ["user", "moderator", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be: user, moderator, or admin")
    
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Проверяем, что пользователь существует
            cur.execute("SELECT id FROM app_user WHERE id = %s", (user_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="User not found")
            
            # Обновляем роль
            cur.execute(
                "UPDATE app_user SET role = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (new_role, user_id)
            )
            
            conn.commit()
            return {"message": f"User role updated to {new_role}"}
        finally:
            cur.close()


@router.put("/{user_id}/verify", summary="Подтвердить email пользователя (только для модераторов)")
def verify_user_email(
    user_id: int,
    moderator_role: str = Depends(require_moderator())
):
    """Подтверждает email пользователя"""
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE app_user SET is_email_verified = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (user_id,)
            )
            
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
            
            conn.commit()
            return {"message": "User email verified"}
        finally:
            cur.close()


@router.delete("/{user_id}", summary="Удалить пользователя (только для админов)")
def delete_user(
    user_id: int,
    admin_role: str = Depends(require_admin())
):
    """Удаляет пользователя"""
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Проверяем, что пользователь существует
            cur.execute("SELECT id FROM app_user WHERE id = %s", (user_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="User not found")
            
            # Удаляем пользователя (CASCADE удалит связанные записи)
            cur.execute("DELETE FROM app_user WHERE id = %s", (user_id,))
            
            conn.commit()
            return {"message": "User deleted successfully"}
        finally:
            cur.close()


@router.get("/stats", summary="Статистика пользователей (только для админов)")
def get_user_stats(admin_role: str = Depends(require_admin())):
    """Получает статистику пользователей"""
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Общая статистика
            cur.execute("SELECT COUNT(*) FROM app_user")
            total_users = cur.fetchone()[0]
            
            # Статистика по ролям
            cur.execute("SELECT role, COUNT(*) FROM app_user GROUP BY role")
            role_stats = {row[0]: row[1] for row in cur.fetchall()}
            
            # Статистика по верификации
            cur.execute("SELECT COUNT(*) FROM app_user WHERE is_email_verified = TRUE")
            verified_users = cur.fetchone()[0]
            
            # Новые пользователи за последние 30 дней
            cur.execute(
                "SELECT COUNT(*) FROM app_user WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'"
            )
            new_users_30d = cur.fetchone()[0]
            
            return {
                "total_users": total_users,
                "verified_users": verified_users,
                "unverified_users": total_users - verified_users,
                "role_distribution": role_stats,
                "new_users_30d": new_users_30d
            }
        finally:
            cur.close()

