import datetime
from typing import Any

from jwt_functions import InvalidTokenError

from core.settings import settings
from jose import jwt, ExpiredSignatureError
from datetime import datetime as dt


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
