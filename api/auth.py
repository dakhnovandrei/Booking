from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import settings
from core.database import get_session
from jwt_functions import get_current_user
from repositories.user_repo import UserRepo
from schemas.exception_schemas import UserAlreadyExist, UserDidntExist
from schemas.user_schemas import UserRegister, AuthResponse, UserLogin
from services.user_service import UserService

router = APIRouter()


@router.post('/reg', tags=['User_Auth'])
async def register(user_data: UserRegister, session: AsyncSession = Depends(get_session)):
    user_repo = UserRepo(session)
    user_service = UserService(user_repo)
    try:
        async with session.begin():
            reg_user = await user_service.register(user_data)
        return {'detail': f'Зарегистрирован новый пользователь {reg_user.id}'}
    except UserAlreadyExist:
        raise HTTPException(status_code=409, detail='Пользователь уже существует')
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Почта уже зарегистрирована")


@router.post('/login', tags=['User_Auth'], response_model=AuthResponse)
async def login(user_data: UserLogin, response: Response, session: AsyncSession = Depends(get_session)):
    user_repo = UserRepo(session)
    user_service = UserService(user_repo)
    try:
        access_token, refresh_token = await user_service.login(user_data)
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            max_age=settings.ACCESS_TOKEN_LIFETIME * 60,
            secure=True,  # Change if u go into production
            samesite='lax'
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            max_age=settings.REFRESH_TOKEN_LIFETIME * 60,
            secure=False,  # Change if u go into production
            samesite='lax'
        )
        return AuthResponse(access_token=access_token, refresh_token=refresh_token)
    except UserDidntExist:
        raise HTTPException(status_code=401, detail='Неверный email или пароль')


@router.post('/refresh')
async def refresh(response: Response, refresh_token: str | None = Cookie(default=None),
                  session: AsyncSession = Depends(get_session)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail='Отсутствует refresh токен')
    user_repo = UserRepo(session)
    user_service = UserService(user_repo)
    try:
        new_access = await user_service.refresh_access_token(refresh_token)

        response.set_cookie(
            key='access_token',
            max_age=settings.ACCESS_TOKEN_LIFETIME * 60,
            value=new_access,
            httponly=True,
            secure=False,
            samesite='lax',
        )
    except Exception:
        raise HTTPException(status_code=401, detail='Невалидный refresh token')


@router.post('/logout')
def logout(response: Response):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return {'detail': "Вы успешно вышли из аккаунта"}
