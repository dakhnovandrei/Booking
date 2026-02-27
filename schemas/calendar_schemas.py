from decimal import Decimal

from pydantic import BaseModel, Field
import datetime as dt


class AvailabilityCalendar(BaseModel):
    property_id: int = Field()
    date: dt.date = Field
    price: Decimal = Field
    booking_id: int | None = Field
    is_available: bool = Field
    is_blocked: bool = Field
    is_checked_out: bool = Field
