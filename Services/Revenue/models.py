from pydantic import BaseModel


class RevenueData(BaseModel):
    totalBookings: int
    totalRevenue: int
    lastMonthBookings: int
    lastMonthRevenue: int
    currentMonthBookings: int
    currentMonthRevenue: int