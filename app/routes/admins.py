from fastapi import APIRouter, Depends, Response, Request
from app.Security.JWT_config import security
from sqlalchemy import select
from app.Security.JWT_config import JWT_config
from app.database.database import SessionDep
from app.database.models import Admin_Model, User_Model, transaction_model
from app.schemas.admin import CreateAdmin
from app.Security.auth import get_current_admin_role, get_current_admin_uid
router = APIRouter(
    prefix="/admins",
    tags=["Admins"] 
)


@router.get("/users", dependencies=[Depends(security.access_token_required)])
async def get_all_users(session: SessionDep):
    query = select(User_Model)
    result = await session.execute(query)
    users = result.scalars().all()
    return {"users": [{"user_id": user.id, "balance": user.balance} for user in users]}

@router.post("/login")
async def admin_login(token: str, response: Response, session: SessionDep):
    query = select(Admin_Model).where(Admin_Model.token == token)
    result = await session.execute(query)
    admin = result.scalar_one_or_none()
    if admin:
        custom_claims = {"role": str(admin.role)}
        JWT_token = security.create_access_token(uid=str(admin.id), data=custom_claims)
        response.set_cookie(JWT_config.JWT_ACCESS_COOKIE_NAME, JWT_token)
        return {"message": "Admin logged in successfully"}
    else:
        return {"error": "Invalid token"}
    

@router.get("/check_role", dependencies=[Depends(security.access_token_required)])
async def check_admin_role(request: Request):
    role = get_current_admin_role(request)
    return {"role": role}

@router.post("/add_admin")
async def add_admin(admin_data:CreateAdmin, session: SessionDep, request: Request):
    current_role = get_current_admin_role(request)
    if current_role != "superadmin":
        return {"error": "Access denied. Only superadmins can add new admins."}
    
    new_admin = Admin_Model(token=admin_data.token, role=admin_data.role)
    session.add(new_admin)
    await session.commit()
    return {"message": "New admin added successfully"}


@router.post("/delete_admin")
async def delete_admin(id: int, session: SessionDep, request: Request):
    current_role = get_current_admin_role(request)
    if current_role != "superadmin":
        return {"error": "Access denied. Only superadmins can delete admins."}
    
    query = select(Admin_Model).where(Admin_Model.id == id)
    result = await session.execute(query)
    admin_to_delete = result.scalar_one_or_none()
    
    if admin_to_delete:
        await session.delete(admin_to_delete)
        await session.commit()
        return {"message": "Admin deleted successfully"}
    else:
        return {"error": "Admin not found"}

@router.get("/get_admins")
async def get_admins(session: SessionDep, request: Request):
    current_role = get_current_admin_role(request)
    if current_role != "superadmin":
        return {"error": "Access denied. Only superadmins can delete admins."}
    
    query = select(Admin_Model)
    result = await session.scalars(query)
    all_admins = result.all()
    return {"admins": [{"id": admin.id, "token": admin.token, "role": admin.role} for admin in all_admins]}

@router.post("/change_price")
async def change_price(new_price: int, session: SessionDep, request:Request):
    current_uid = get_current_admin_uid(request)
    query = select(Admin_Model).where(Admin_Model.id == current_uid)
    result = await session.execute(query)
    admin_to_change_price = result.scalar_one_or_none()
    if admin_to_change_price:
        admin_to_change_price.price = new_price
        await session.commit()
        return {"message": "Admin price changed successfully"}
    else:
        return {"error": "Admin not found"}

@router.post("/change_user_balance", dependencies=[Depends(security.access_token_required)])
async def change_user_balance_post(user_id: int, session: SessionDep, request: Request):
    return await change_user_balance(user_id, session, request)

@router.get("/change_user_balance", dependencies=[Depends(security.access_token_required)])
async def change_user_balance_get(user_id: int, session: SessionDep, request: Request):
    return await change_user_balance(user_id, session, request)



async def change_user_balance(user_id: int, session: SessionDep, request:Request):
    current_uid = get_current_admin_uid(request)
    query = select(User_Model).where(User_Model.id == user_id)
    result = await session.execute(query)
    user_to_change_balance = result.scalar_one_or_none()
    if user_to_change_balance:
        query = select(Admin_Model).where(Admin_Model.id == current_uid)
        result = await session.execute(query)
        admin_to_change_balance = result.scalar_one_or_none()
        if not admin_to_change_balance:
            return {"error": "Admin not found"}
        if admin_to_change_balance.price is not None:
            user_to_change_balance.balance = user_to_change_balance.balance + admin_to_change_balance.price
            if user_to_change_balance.balance < 0:
                return {"error": "Dont have enough balance"}
            new_transaction = transaction_model(sender = current_uid, recipient = user_id, count = admin_to_change_balance.price)
            session.add(new_transaction)
            await session.commit()
            return {"message": "User balance changed successfully"}
        else:
            return {"message": "Admin price empty"}
    else:
        return {"error": "Admin not found"}


@router.get("/check_price")
async def check_price(session: SessionDep, request: Request):
    current_uid = get_current_admin_uid(request)
    query = select(Admin_Model).where(Admin_Model.id == current_uid)
    result = await session.execute(query)
    admin = result.scalar_one_or_none()
    if admin: 
        return {"ok": "True", "Admin token": {admin.token}, "Admin price": {admin.price}}
    else:
        return {"ok": "False"}