from pydantic import BaseModel
from datetime import datetime, date


class BookingResponse(BaseModel):
    id: int
    pitch_name: str
    ground_id: int
    user_email: str
    user_contact_no: str
    start_time: datetime
    duration: str
    end_time: datetime
    payment_status: str
    booking_date: date
