import base64

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from Database.async_tables import get_grounds_table, get_ground_owners_table, get_ground_images_table
from .models import GroundListModel


# async def get_grounds_for_owner(current_user: str, db: AsyncSession) -> List[GroundListModel]:
#     try:
#         grounds_table = await get_grounds_table()
#         ground_owners_table = await get_ground_owners_table()
#         query = (
#             select(
#                 grounds_table.c.id,
#                 grounds_table.c.name,
#                 grounds_table.c.address
#             )
#             .select_from(
#                 grounds_table.join(
#                     ground_owners_table,
#                     grounds_table.c.id == ground_owners_table.c.ground_id
#                 )
#             )
#             .where(ground_owners_table.c.owner_email == current_user)
#         )
#
#         result = await db.execute(query)
#         rows = result.fetchall()
#
#         # Map rows to GroundListModel
#         return [
#             GroundListModel(
#                 id=row.id,
#                 name=row.name,
#                 address=row.address
#             )
#             for row in rows
#         ]
#
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error fetching grounds: {str(e)}"
#         )
# async def get_grounds_for_owner(current_user: str, db: AsyncSession) -> List[GroundListModel]:
#     try:
#         grounds_table = await get_grounds_table()
#         ground_owners_table = await get_ground_owners_table()
#         ground_images_table = await get_ground_images_table()
#
#         query = (
#             select(
#                 grounds_table.c.id,
#                 grounds_table.c.name,
#                 grounds_table.c.address,
#                 func.coalesce(ground_images_table.c.image_data, None).label("image_data")
#             )
#             .select_from(
#                 grounds_table
#                 .join(ground_owners_table, grounds_table.c.id == ground_owners_table.c.ground_id)
#                 .outerjoin(ground_images_table, grounds_table.c.id == ground_images_table.c.ground_id)
#             )
#             .where(ground_owners_table.c.owner_email == current_user)
#             .group_by(grounds_table.c.id, ground_images_table.c.image_data)
#         )
#
#         result = await db.execute(query)
#         rows = result.fetchall()
#
#         # Map rows to GroundListModel, encoding image data in Base64 if available
#         return [
#             GroundListModel(
#                 id=row.id,
#                 name=row.name,
#                 address=row.address,
#                 photo=base64.b64encode(row.image_data).decode('utf-8') if row.image_data else None
#             )
#             for row in rows
#         ]
#
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error fetching grounds: {str(e)}"
#         )
async def get_grounds_for_owner(current_user: str, db: AsyncSession) -> List[GroundListModel]:
    try:
        grounds_table = await get_grounds_table()
        ground_owners_table = await get_ground_owners_table()
        ground_images_table = await get_ground_images_table()

        # Subquery to select one image per ground ID
        subquery = (
            select(
                ground_images_table.c.ground_id,
                ground_images_table.c.image_data
            )
            .distinct(ground_images_table.c.ground_id)  # Ensures one image per ground ID
            .subquery()
        )

        query = (
            select(
                grounds_table.c.id,
                grounds_table.c.name,
                grounds_table.c.address,
                func.coalesce(subquery.c.image_data, None).label("image_data")
            )
            .select_from(
                grounds_table
                .join(ground_owners_table, grounds_table.c.id == ground_owners_table.c.ground_id)
                .outerjoin(subquery, grounds_table.c.id == subquery.c.ground_id)
            )
            .where(ground_owners_table.c.owner_email == current_user)
        )

        result = await db.execute(query)
        rows = result.fetchall()

        # Map rows to GroundListModel, encoding image data in Base64 if available
        return [
            GroundListModel(
                id=row.id,
                name=row.name,
                address=row.address,
                photo=base64.b64encode(row.image_data).decode('utf-8') if row.image_data else None
            )
            for row in rows
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching grounds: {str(e)}"
        )
