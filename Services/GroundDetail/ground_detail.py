import base64
from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from Database.async_tables import get_ground_images_table, get_pitches_table, get_grounds_table, \
    get_ground_facilities_table, get_ground_equipments_table, get_user_reviews_table
from .models import PitchResponseModel, GroundResponseModel


async def get_ground_detail(id: int, db: AsyncSession) -> GroundResponseModel:
    ground_table = await get_grounds_table()
    query = select(ground_table).where(ground_table.c.id == id)
    result = await db.execute(query)
    row = result.mappings().first()  # Fetch the first row matching the query

    if not row:
        raise HTTPException(status_code=404, detail="Ground not found")

    # Convert the result into a Pydantic model
    ground_detail = GroundResponseModel(**row)
    ground_detail.rating = round(ground_detail.rating, 1)
    return ground_detail


async def get_ground_images(id: int, db: AsyncSession):
    ground_img = await get_ground_images_table()
    query = select(ground_img.c.image_data).where(ground_img.c.ground_id == id)
    result = await db.stream(query)

    images_base64 = []

    async for row in result:
        image_data = row[0]  # `row` is a tuple, and image_data is the first element
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        images_base64.append(image_base64)

    if not images_base64:
        raise HTTPException(status_code=404, detail="No images found for the specified ground ID")
    return JSONResponse(content={"images": images_base64})


async def get_pitches(ground_id: int, db: AsyncSession) -> List[PitchResponseModel]:
    pitch_table = await get_pitches_table()
    query = select(pitch_table).where(pitch_table.c.ground_id == int(ground_id))
    result = await db.execute(query)
    rows = result.mappings().all()
    pitches = [PitchResponseModel(**row) for row in rows]

    return pitches


async def get_facilities(ground_id: int, db: AsyncSession) -> List[str]:
    try:
        facility_table = await get_ground_facilities_table()  # Get the table dynamically
        query = select(facility_table.c.facility).where(facility_table.c.ground_id == ground_id)
        result = await db.execute(query)
        rows = result.scalars().all()  # Use scalars to extract single column values

        return rows
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


async def get_equipments(ground_id: int, db: AsyncSession) -> List[str]:
    try:
        equipments_table = await get_ground_equipments_table()  # Get the table dynamically
        query = select(equipments_table.c.equipment).where(equipments_table.c.ground_id == ground_id)
        result = await db.execute(query)
        rows = result.scalars().all()  # Use scalars to extract single column values

        return rows
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


async def get_reviews_by_ground(ground_id: int, db: AsyncSession):
    user_reviews = await get_user_reviews_table()

    # Query to fetch reviews for the specified ground_id
    query = select(user_reviews).where(user_reviews.c.ground_id == ground_id)
    result = await db.execute(query)
    reviews = result.fetchall()

    # If no reviews are found, raise a 404 error
    if not reviews:
        raise HTTPException(status_code=404, detail=f"No reviews found for ground ID {ground_id}")

    # Format and return the results
    return [
        {
            "user_id": review.user_id,
            "rating": review.rating,
            "ground_id": review.ground_id,
            "comment": review.comment,
        }
        for review in reviews
    ]
