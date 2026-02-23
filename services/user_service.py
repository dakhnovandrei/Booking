from authx.exceptions import InvalidToken
from fastapi import Cookie
from jose import ExpiredSignatureError
from jwt import InvalidTokenError
from jwt_functions import create_access_token, create_refresh_token, decode_access_token
from repositories.user_repo import UserRepo
from schemas.user_schemas import UserRegister, UserLogin, AuthResponse, UserUpdate
from schemas.exception_schemas import UserAlreadyExist, UserDidntExist, UserNotFound
from passlib.hash import bcrypt


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def register(self, user_data: UserRegister):
        existing_email = await self.user_repo.get_user_by_email(user_data.email)
        if existing_email:
            raise UserAlreadyExist('Email уже зарегистрирован')
        if user_data.phone:
            existing_phone = await self.user_repo.get_user_by_phone(user_data.phone)
            if existing_phone:
                raise UserAlreadyExist('Номер телефона уже зарегистрирован')

        hashed_password = bcrypt.using(rounds=12).hash(user_data.password)
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict['password'] = hashed_password

        user = await self.user_repo.create_user(user_data=UserRegister(**user_dict))
        return user

    async def login(self, user_log: UserLogin) -> AuthResponse:
        existing_user = await self.user_repo.get_user_by_email(user_log.email)

        if not existing_user or bcrypt.verify(user_log.password, existing_user.password):
            raise UserDidntExist('Неправильная почта или пароль')

        access_token = create_access_token({'sub': existing_user.id, 'role': existing_user.user_type})
        refresh_token = create_refresh_token({'sub': existing_user.id, 'role': existing_user.user_type})

        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def get_user_profile(self, access_token: str = Cookie(...)):
        try:
            payload = decode_access_token(access_token)
        except ExpiredSignatureError:
            raise InvalidToken('Токен просрочен')
        except InvalidTokenError:
            raise InvalidToken('Ошибка в токене')

        user = await self.user_repo.get_user_by_id(payload['sub'])
        if not user:
            raise UserNotFound(f'Пользователя с id: {payload["sub"]} не существует')

        return user

    async def delete_user(self, user_id: int):
        """
        Удаляет пользователя.
        Если пользователя нет — кидает UserNotFound.
        """
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFound(f"Пользователь с id {user_id} не найден")

        await self.user_repo.delete_user(user)

    async def update_user(self, user_id: int, user_data: UserUpdate):
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
