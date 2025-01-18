from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Services.GroundDetail.ground_detail import get_ground_detail, get_pitches, get_ground_images, get_facilities, \
    get_equipments, get_reviews_by_ground
from Database.Async_DB_Connection import get_db
from Services.GroundDetail.models import PitchResponseModel

router = APIRouter(
    prefix="/ground_detail",
    tags=["GroundDetail"],
)

@router.get("/{ground_id}")
async def get_ground(ground_id: int, db: AsyncSession = Depends(get_db)):
    try:
        id = int(ground_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid id format")
    return await get_ground_detail(id=id, db=db)

@router.get("/groundimages/{images_id}")
async def get_images(images_id: int, db: AsyncSession = Depends(get_db)):
    try:
        images_id = int(images_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid ID format")
    return await get_ground_images(id=images_id, db=db)


@router.get("/ground_detail/pitches/{ground_id}", response_model=List[PitchResponseModel])
async def get_ground_pitches(ground_id, db: AsyncSession = Depends(get_db)):
    return await get_pitches(ground_id=ground_id, db=db)


@router.get("/facilities/{ground_id}", response_model=List[str])
async def get_facilities_router(ground_id: int, db: AsyncSession = Depends(get_db)):
    return await get_facilities(ground_id=ground_id, db=db)


@router.get("/equipments/{ground_id}", response_model=List[str])
async def get_equipments_router(ground_id: int, db: AsyncSession = Depends(get_db)):
    return await get_equipments(ground_id=ground_id, db=db)


@router.get('/reviews/{id}')
async def get_reviews(id: int, db: AsyncSession = Depends(get_db)):
    return await get_reviews_by_ground(ground_id=id, db=db)




