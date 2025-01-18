from fastapi import APIRouter, Depends
from Database.Async_DB_Connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from Services.Bookings.booking import get_ground_bookings, update_booking_payment
from Services.Auth.auth import get_current_user

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)


@router.get("/{ground_id}")
async def get_bookings(ground_id: int, current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_ground_bookings(ground_id=ground_id, current_user_email=current_user, db=db)


@router.post("/update/{booking_id}")
async def update_payment(booking_id: int, status: dict, db: AsyncSession = Depends(get_db)):
    status = status["payment"]
    return await update_booking_payment(booking_id=booking_id, payment_status=status, db=db)
