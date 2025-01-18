from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Database.Async_DB_Connection import get_db
from Services.OwnerDetails.owner_details import get_owner_info

router = APIRouter(
    prefix="/owner_details",
    tags=["Owner Details"],
)


@router.get("/{email}")
async def get_owner_details(email: str, db: AsyncSession = Depends(get_db)):
    return await get_owner_info(email=email, db=db)
