from fastapi import APIRouter, Depends
from jwt_functions import get_current_user

router = APIRouter(prefix='/users')


@router.get('/me')
async def get_users_profile(user=Depends(get_current_user)):
    return user
