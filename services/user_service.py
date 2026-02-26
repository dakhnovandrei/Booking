from typing import Tuple, Any
from passlib.context import CryptContext
from authx.exceptions import InvalidToken
from fastapi import Cookie
from jose import ExpiredSignatureError
from jwt import InvalidTokenError
from jwt_functions import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from repositories.user_repo import UserRepo
from schemas.user_schemas import UserRegister, UserLogin, AuthResponse, UserUpdate
from schemas.exception_schemas import UserAlreadyExist, UserDidntExist, UserNotFound
from models import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserService:
    """
    Сервис для выполнения различных методов с пользователями:
    Регистрация, Авторизация, Обновления
    """

    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def register(self, user_data: UserRegister) -> User:
        """
        Регистрация пользователя, проверка почты и телефона, хэширование пароля и добавление в бд
        :param user_data:
        :return: User object
        """
        existing_email = await self.user_repo.get_user_by_email(user_data.email)
        if existing_email:
            raise UserAlreadyExist('Email уже зарегистрирован')
        if user_data.phone:
            existing_phone = await self.user_repo.get_user_by_phone(user_data.phone)
            if existing_phone:
                raise UserAlreadyExist('Номер телефона уже зарегистрирован')
        password_bytes = user_data.password.encode('utf-8')
        hashed_password = pwd_context.hash(password_bytes)
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict['password'] = hashed_password

        user = await self.user_repo.create_user(user_data=UserRegister(**user_dict))
        return user

    async def login(self, user_log: UserLogin) -> Tuple[Any, Any]:
        """
        Реализация авторизации с помощью JWT токенов
        Проверка существования пользователя, сравнение паролей
        Создание access и refresh токенов
        :param user_log:
        :return: AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
        """
        existing_user = await self.user_repo.get_user_by_email(user_log.email)
        password_bytes = user_log.password.encode('utf-8')
        if not existing_user or pwd_context.verify(password_bytes, existing_user.password):
            raise UserDidntExist('Неправильная почта или пароль')

        access_token = create_access_token({'sub': str(existing_user.id), 'role': existing_user.user_type})
        refresh_token = create_refresh_token({'sub': str(existing_user.id), 'role': existing_user.user_type})

        return access_token, refresh_token

    async def get_user_profile(self, access_token: str = Cookie(...)) -> User:
        """
        Получение информации по пользователю с помощью id из access_token
        Попытки поймать ошибки связанные с длительностью жизни токена и его верности.
        :param access_token:
        :return: User obj
        """
        try:
            payload = decode_access_token(access_token)
        except ExpiredSignatureError:
            raise InvalidToken('Токен просрочен')
        except InvalidTokenError:
            raise InvalidToken('Ошибка в токене')

        user = await self.user_repo.get_user_by_id(int(payload['sub']))
        if not user:
            raise UserNotFound(f'Пользователя с id: {int(payload["sub"])} не существует')

        return user

    async def delete_user(self, user_id: int) -> None:
        """
        Удаляет пользователя.
        Если пользователя нет — кидает UserNotFound.
        """
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFound(f"Пользователь с id {user_id} не найден")

        await self.user_repo.delete_user(user)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """
        Обновляет заполненные поля пользователя.
        Проверка регистрации предоставляемых номера и почты.
        :param user_id:
        :param user_data:
        :return: User obj
        """
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFound(f'Пользователь с id: {user_id} не найден')
        if user_data.email and user_data.email != user.email:
            existing_email = await self.user_repo.get_user_by_email(user_data.email)
            if existing_email:
                raise UserAlreadyExist("Данный адрес электронной почты уже зарегистрирован")
        if user_data.phone and user_data.phone != user.phone:
            existing_phone = await self.user_repo.get_user_by_phone(user_data.phone)
            if existing_phone:
                raise UserAlreadyExist("Данный номер телефона уже зарегистрирован")

        updated_user = await self.user_repo.update(user, user_data)

        return updated_user

    async def refresh_access_token(self, refresh_token: str) -> str:
        payload = decode_refresh_token(refresh_token)
        user_id = payload.get('sub')
        user = await self.user_repo.get_user_by_id(int(user_id))
        if not user:
            raise UserNotFound("Пользователь не найден")
        new_access_token = create_access_token({
            'sub': str(user.id),
            'role': user.user_type
        })
        return new_access_token
