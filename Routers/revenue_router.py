
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Async_DB_Connection import get_db
from Services.Revenue.models import RevenueData
from Services.Revenue.revenue import get_ground_revenue

router = APIRouter(
    prefix="/revenue",
    tags=["Revenue"],
)

@router.get("/{ground_id}", response_model=RevenueData)
async def get_revenue_data(ground_id: int, db: AsyncSession = Depends(get_db)):
    return await get_ground_revenue(ground_id=ground_id, session=db)
