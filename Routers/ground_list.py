from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Services.GroundSelection.ground_list import get_grounds_for_owner
from Database.Async_DB_Connection import get_db
from Services.GroundSelection.models import GroundListModel
from Services.Auth.auth import get_current_user

router = APIRouter(
    prefix="/ground_list",
    tags=["Ground List"],
)


@router.get("/", response_model=List[GroundListModel])
async def get_ground_list(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_grounds_for_owner(current_user, db)
