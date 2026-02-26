from sqlalchemy import select, delete
from schemas.user_schemas import UserRegister, UserUpdate
from models import User


class UserRepo:
    """
    Репозиторий реализовывающий взаимодействия юзера с базой данных
    """
    model = User

    def __init__(self, session):
        self.session = session

    async def create_user(self, user_data: UserRegister) -> User:
        """
        Создание нового пользователя в базе данных
        :param user_data:
        :return: User obj
        """
        new_instance = self.model(**user_data.model_dump())
        self.session.add(new_instance)
        await self.session.commit()
        await self.session.refresh(new_instance)
        return new_instance

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Получение пользователя по почте
        :param email:
        :return: User obj
        """
        user = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )
        return user.scalar_one_or_none()

    async def get_user_by_id(self, us_id: int) -> User | None:
        """
        Получение пользователя по id
        :param us_id:
        :return: User obj
        """
        user = await self.session.execute(
            select(self.model).where(self.model.id == us_id)
        )
        return user.scalar_one_or_none()

    async def get_user_by_phone(self, phone: str) -> User | None:
        """
        Получение пользователя по номеру телефона
        :param phone:
        :return: User obj
        """
        user = await self.session.execute(
            select(self.model).where(self.model.phone == phone)
        )
        return user.scalar_one_or_none()

    async def update(self, user: User, data: UserUpdate) -> User:
        """
        Обновление указанных полей пользователя
        :param user:
        :param data:
        :return: User obj
        """
        updated_data = data.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user: User) -> None:
        """
        Удаление пользователя
        :param user:
        :return: None
        """
        await self.session.delete(user)
        await self.session.commit()
