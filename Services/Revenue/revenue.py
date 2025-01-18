from datetime import datetime, timedelta

from sqlalchemy import select, func, case, text, Integer, and_
from sqlalchemy.ext.asyncio import AsyncSession

from Database.async_tables import get_bookings_table, get_pitches_table
from .models import RevenueData


async def get_ground_revenue(session: AsyncSession, ground_id: int) -> RevenueData:
    bookings = await get_bookings_table()
    pitches = await get_pitches_table()

    # Define the date ranges
    current_date = datetime.utcnow()
    first_day_this_month = current_date.replace(day=1)
    first_day_last_month = (first_day_this_month - timedelta(days=1)).replace(day=1)
    last_day_last_month = first_day_this_month - timedelta(days=1)

    # Query for total bookings and revenue
    total_query = select(
        func.count(bookings.c.id).label("total_bookings"),
        func.sum(
            case(
                (bookings.c.duration == text("'60 minutes'"), pitches.c.price_per_60mins),
                else_=pitches.c.price_per_90mins,
            ).cast(Integer)
        ).label("total_revenue")
    ).select_from(bookings.join(pitches)).where(
        and_(bookings.c.payment_status == 'paid', bookings.c.ground_id == ground_id)
    )

    # Query for last month's bookings and revenue
    last_month_query = select(
        func.count(bookings.c.id).label("last_month_bookings"),
        func.sum(
            case(
                (bookings.c.duration == text("'60 minutes'"), pitches.c.price_per_60mins),
                else_=pitches.c.price_per_90mins,
            ).cast(Integer)
        ).label("last_month_revenue")
    ).select_from(bookings.join(pitches)).where(
        and_(
            bookings.c.payment_status == 'paid',
            bookings.c.ground_id == ground_id,
            bookings.c.booking_date >= first_day_last_month,
            bookings.c.booking_date <= last_day_last_month,
        )
    )

    # Query for this month's bookings and revenue
    current_month_query = select(
        func.count(bookings.c.id).label("current_month_bookings"),
        func.sum(
            case(
                (bookings.c.duration == text("'60 minutes'"), pitches.c.price_per_60mins),
                else_=pitches.c.price_per_90mins,
            ).cast(Integer)
        ).label("current_month_revenue")
    ).select_from(bookings.join(pitches)).where(
        and_(
            bookings.c.payment_status == 'paid',
            bookings.c.ground_id == ground_id,
            bookings.c.booking_date >= first_day_this_month,
        )
    )

    # Execute the queries
    total_result = await session.execute(total_query)
    last_month_result = await session.execute(last_month_query)
    current_month_result = await session.execute(current_month_query)

    # Fetch the results
    total_data = total_result.fetchone()
    last_month_data = last_month_result.fetchone()
    current_month_data = current_month_result.fetchone()

    # Return the aggregated data as a RevenueData object
    return RevenueData(
        totalBookings=total_data.total_bookings or 0,
        totalRevenue=total_data.total_revenue or 0,
        lastMonthBookings=last_month_data.last_month_bookings or 0,
        lastMonthRevenue=last_month_data.last_month_revenue or 0,
        currentMonthBookings=current_month_data.current_month_bookings or 0,
        currentMonthRevenue=current_month_data.current_month_revenue or 0,
    )
