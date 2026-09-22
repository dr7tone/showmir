
from typing import cast

from fastapi import APIRouter
from sqlalchemy import Table

from app.database.models import Admin_Model, User_Model, transaction_model
from app.database.database import SessionDep, engine
router = APIRouter(
    prefix="/db",
    tags=["DB"] 
)






@router.post("/create_table_for_users") # запороленный(ну или почти) сброс БД для пользователей
async def create_table_for_users(data: str):
    if data == "drop and create":
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: User_Model.metadata.drop_all(bind=sync_conn, tables=[cast(Table, User_Model.__table__)]))
            await conn.run_sync(lambda sync_conn: User_Model.metadata.create_all(bind=sync_conn, tables=[cast(Table, User_Model.__table__)]))
        return {"ok": True}
    else:
        return {"ok": False, "message": "Invalid data. To create the table, send 'drop and create'."}


@router.post("/create_table_for_admins") # запороленный(ну или почти) сброс БД для админов
async def create_table_for_admins(data: str, session: SessionDep):
    if data == "drop and create":
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: Admin_Model.metadata.drop_all(bind=sync_conn, tables=[cast(Table, Admin_Model.__table__)]))
            await conn.run_sync(lambda sync_conn: Admin_Model.metadata.create_all(bind=sync_conn, tables=[cast(Table, Admin_Model.__table__)]))
        superadmin = Admin_Model(token="superadmin", role="superadmin") 
        session.add(superadmin)
        await session.commit()
        return {"ok": True}
    
    else:
        return {"ok": False, "message": "Invalid data. To create the table, send 'drop and create'."}

@router.post("/create_table_for_transactions")
async def create_table_for_transactions():
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: transaction_model.metadata.drop_all(bind=sync_conn, tables=[cast(Table, transaction_model.__table__)]))
        await conn.run_sync(lambda sync_conn: transaction_model.metadata.create_all(bind=sync_conn, tables=[cast(Table, transaction_model.__table__)]))
    return {"ok": True}
