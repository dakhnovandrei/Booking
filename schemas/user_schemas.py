from pydantic import BaseModel, EmailStr, Field, validator
from sql_enums import UserType
import re


class UserRegister(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100, examples='Alex')
    second_name: str = Field(..., min_length=2, max_length=100, examples='Volchckov')
    password: str = Field(..., min_length=8, max_length=50)
    user_type: UserType
    email: EmailStr = Field(..., min_length=3, max_length=200, examples='example@mail.ru')
    phone: str = Field(..., examples='+79123126775')

    @validator(phone)
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not re.match(r'^\+\d{5,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
        return value


class UserUpdate(BaseModel):
    first_name: str | None
    first_name: str | None = Field(..., min_length=2, max_length=100, examples='Alex')
    second_name: str | None = Field(..., min_length=2, max_length=100, examples='Volchckov')
    password: str | None = Field(..., min_length=8, max_length=50)
    user_type: UserType | None
    email: EmailStr | None = Field(..., min_length=3, max_length=200, examples='example@mail.ru')
    phone: str | None = Field(..., examples='+79123126775')


class UserLogin(BaseModel):
    email: EmailStr = Field(..., min_length=3, max_length=200, examples='example@mail.ru')
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
