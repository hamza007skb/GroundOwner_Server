from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from Database.async_tables import get_ground_owners_table, get_bookings_table
from .model import BookingResponse


async def get_ground_bookings(ground_id: int, db: AsyncSession, current_user_email: str) -> list[BookingResponse]:
    try:
        ground_owners_table = await get_ground_owners_table()
        bookings_table = await get_bookings_table()

        # Verify if the user is authorized to access the ground
        query = select(ground_owners_table).where(
            ground_owners_table.c.ground_id == ground_id,
            ground_owners_table.c.owner_email == current_user_email,
        )
        result = await db.execute(query)
        ground_owner = result.fetchone()

        if not ground_owner:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access bookings for this ground.",
            )

        # Fetch bookings for the specific ground
        bookings_query = select(bookings_table).where(bookings_table.c.ground_id == ground_id)
        bookings_result = await db.execute(bookings_query)
        bookings = bookings_result.fetchall()

        # Map the results to BookingResponse model
        booking_responses = [
            BookingResponse(
                id=booking["id"],
                pitch_name=booking["pitch_name"],
                ground_id=booking["ground_id"],
                user_email=booking["user_email"],
                user_contact_no=booking["user_contact_no"],
                start_time=booking["start_time"],
                duration=str(booking["duration"]),
                end_time=booking["end_time"],
                payment_status=booking["payment_status"],
                booking_date=booking["booking_date"],
            )
            for booking in (row._mapping for row in bookings)
        ]

        return booking_responses

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


async def update_booking_payment(booking_id: int, payment_status: str, db: AsyncSession):
    try:
        bookings_table = await get_bookings_table()
        query = select(bookings_table).where(bookings_table.c.id == booking_id)
        result = await db.execute(query)
        bookings = result.fetchall()

        if not bookings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No bookings found."
            )

        # Update payment_status for all bookings with the specified ground_id
        update_query = (
            update(bookings_table)
            .where(bookings_table.c.id == booking_id)
            .values(payment_status=payment_status)
        )
        await db.execute(update_query)
        await db.commit()

        return {"message": f"Payment status updated to '{payment_status}' for booking {booking_id}."}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating payment status: {str(e)}",
        )
