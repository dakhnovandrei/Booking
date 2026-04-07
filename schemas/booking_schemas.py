from decimal import Decimal

from pydantic import BaseModel, Field
from datetime import datetime

from sql_enums import BookingStatus, PaymentStatus


class BookingCreate(BaseModel):
    property_id: int = Field()
    guest_id: int = Field()
    guest_cnt: int = Field()

    status: BookingStatus = Field()

    check_in: datetime
    check_out: datetime

    price_per_night: Decimal = Field()
    total_amount: Decimal = Field()

    currency: str

    payment_status: PaymentStatus = Field()
    cancelled: bool = Field()

    cancelled_by: int | None = Field()

    expires_at: datetime
