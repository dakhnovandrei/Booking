import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator, condecimal

from sql_enums import RoomType, RoomStatus, Currency

PriceDecimal = condecimal(
    ge=1,
    le=100_000_000,
    max_digits=12,
    decimal_places=2
)


class RoomCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100, examples=['Студия 22м^2'])
    description: str = Field(min_length=10, max_length=1000, examples=['Красивая студия расположенная там то'])

    country: str = Field(min_length=3, max_length=100, examples=['Россия'])
    city: str = Field(min_length=3, max_length=100, examples=['Москва'])
    address: str = Field(min_length=5, max_length=250, examples=['Молодежная улица дом 5 корпус 3'])

    property_type: RoomType

    guests_cnt: int = Field(ge=1, examples=[2])
    bedrooms: int = Field(ge=1, examples=[1])
    beds: int = Field(ge=1, examples=[5])
    bathrooms: int = Field(ge=1, examples=[2])

    base_price: PriceDecimal
    currency: Currency
    cleaning_fee: PriceDecimal
    security_deposit: Decimal = Field(ge=1.0, le=100_000_000, max_digits=12, decimal_places=2,
                                      examples=[Decimal('12.99')])
    weekend_multiplier: Decimal = Field(ge=1.0, le=100_000_000, max_digits=12, decimal_places=2,
                                        examples=[Decimal('2.50')])

    min_stay: int = Field(ge=1, description='Минимально количество зарезервированных дней')
    max_stay: int = Field(ge=1, description='Максимальное количество зарезервированных дней')

    is_available: bool
    status: RoomStatus

    @model_validator(mode="after")
    def validate_stay_range(self):
        if self.min_stay > self.max_stay:
            raise ValueError("min_stay не может быть больше max_stay")
        return self


class RoomUpdate(BaseModel):
    pass