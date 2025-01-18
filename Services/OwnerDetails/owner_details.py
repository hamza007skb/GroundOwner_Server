import base64

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Database.async_tables import get_owner_images_table, get_owners_table


async def get_owner_info(email: str, db: AsyncSession):
    owners = await get_owners_table()
    owner_image = await get_owner_images_table()

    # Query owner information
    owner_query = select(owners).where(owners.c.email == email)
    owner_result = await db.execute(owner_query)
    owner = owner_result.mappings().first()

    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")

    # Query owner image
    image_query = select(owner_image.c.image_data).where(owner_image.c.owner_email == email)
    image_result = await db.execute(image_query)
    image = image_result.scalar()

    if not image:
        raise HTTPException(status_code=404, detail="Owner image not found")

    # Encode image data to base64 for JSON response
    encoded_image = base64.b64encode(image).decode('utf-8')

    # Prepare response
    response = {
        "email": owner["email"],
        "name": owner["name"],
        "phone_no": owner["phone_no"],
        "image_data": encoded_image
    }

    return response
