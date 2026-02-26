from fastapi import APIRouter, Depends
from jwt_functions import get_current_user

users_router = APIRouter(prefix='/users')


@users_router.get('/me')
async def get_users_profile(user=Depends(get_current_user)):
    return user
