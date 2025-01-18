from fastapi import HTTPException
from Encryption.bcrypt_context import bcrypt_context
from starlette import status
from Database.async_tables import get_owners_table, get_owner_images_table
from datetime import timedelta
from Services.Auth.auth import create_access_token
from Services.Auth.auth_credentials import ACCESS_TOKEN_EXPIRE
from Services.Auth.models import OwnerRequestModel, TokenModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def login_owner(owner_request: OwnerRequestModel, db: AsyncSession) -> TokenModel:
    try:
        owners = await get_owners_table()
        query = select(owners).where(owners.c.email == owner_request.email)
        result = await db.execute(query)
        owner = result.fetchone()

        if not owner:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No user registered with this email",
            )
        if not bcrypt_context.verify(owner_request.password, owner.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
            )

        access_token = create_access_token(
            data={"email": owner.email},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE)
        )
        return TokenModel(
            access_token=access_token,
            token_type="Bearer",
            message="Logged in successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


async def get_owner_image(owner_email: str, db: AsyncSession):
    owner_images = await get_owner_images_table()
    query = select(owner_images).where(owner_images.c.owner_email == owner_email)
    result = await db.execute(query)
    images = result.fetchall()
    if not images:
        raise HTTPException(status_code=404, detail=f"No images found for owner {owner_email}")
    return images.image_data.decode('utf-8', errors='ignore')




