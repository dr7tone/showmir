from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from app.Security.auth import get_current_admin_role
from app.database.database import SessionDep
from app.database.models import User_Model
from app.routes.admins import change_user_balance
router = APIRouter(
    prefix="/users",
    tags=["Users"] 
)

@router.get("/{user_id}")
async def get_user(user_id: int, session: SessionDep, request: Request): #там костыль лютый, если будем делать что то глобальное - надо переделать
    current_role = get_current_admin_role(request)
    if current_role == "admin":
        return await change_user_balance(user_id, session, request)
    else:
        query = select(User_Model).where(User_Model.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return {"user_id": user.id, "balance": user.balance}
        else:
            return {"error": "User not found"}
