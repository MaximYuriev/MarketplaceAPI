from fastapi import APIRouter, Depends

from dependencies.user import current_user, current_admin_user
from schemas.user import UserPayload


user_router = APIRouter(prefix='/user', tags=["User"])


@user_router.get("/info")
def get_info_about_user(user:UserPayload = Depends(current_user)):
    return {"detail": f"Hello, {user.name}"}

@user_router.get("/private_info")
def get_private_info(user: UserPayload = Depends(current_admin_user)):
    return {"detail": f"Hello, {user.name} you are admin! graz!"}
