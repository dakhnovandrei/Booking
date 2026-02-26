import datetime
from typing import Any

from fastapi import Cookie, Depends
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from core.settings import settings
from jose import jwt, ExpiredSignatureError, JWTError
from datetime import datetime as dt

from repositories.user_repo import UserRepo
from schemas.exception_schemas import UserNotFound


def create_token(data: dict, token_type: str,
                 expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    to_encode.update({'token_type': token_type})
    expire = datetime.datetime.utcnow() + (expires_delta or datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_LIFETIME if token_type == 'access' else settings.REFRESH_TOKEN_LIFETIME
    ))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    return create_token(data, 'access', expires_delta)


def create_refresh_token(data: dict, expires_delta: datetime.timedelta | None = None):
    return create_token(data, 'refresh', expires_delta)


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Декодирует JWT access token и проверяет срок жизни.
    Возвращает payload, если токен валидный.
    Бросает исключение, если токен просрочен или некорректный.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        exp = payload.get("exp")
        if exp is None:
            raise InvalidTokenError("Токен не содержит exp")
        if dt.now(datetime.timezone.utc).timestamp() > exp:
            raise ExpiredSignatureError("Токен просрочен")

        return payload

    except ExpiredSignatureError:
        raise ExpiredSignatureError("Access token истёк")
    except InvalidTokenError:
        raise InvalidTokenError("Невалидный access token")


def decode_refresh_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get('type') != 'refresh':
            raise ValueError("Неверный тип токена")
        exp = payload.get('sub')
        if not exp or dt.utcfromtimestamp(exp) < dt.utcnow():
            raise ValueError('Токен истек')
        return payload
    except JWTError:
        raise ValueError("Неверный refresh токен")


async def get_current_user(access_token: str = Cookie(None), session: AsyncSession = Depends(get_session)):
    user_repo = UserRepo(session)
    if not access_token:
        raise UserNotFound('Токен отсутствует')
    try:
        payload = decode_access_token(access_token)
        user_id: int = payload.get('sub')
        if not user_id:
            raise UserNotFound('Неверный токен')
        user = await user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFound("Пользователь не найден")
        return user
    except (JWTError, ValidationError):
        raise UserNotFound('Пользователь не найден')
