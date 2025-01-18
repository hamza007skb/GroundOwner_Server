from fastapi import HTTPException
from starlette import status
from Encryption.bcrypt_context import bcrypt_context
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from Database.async_tables import get_owners_table
from sqlalchemy import select
from .models import OwnerSignUpModel


async def create_owner(owner: OwnerSignUpModel, db: AsyncSession) -> dict:
    try:
        owners = await get_owners_table()
        query = select(owners).where(
            (owners.c.email == owner.email)
        )
        result = await db.execute(query)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email or username already exists."
            )

        hashed_password = bcrypt_context.hash(owner.password)
        insert_stmt = owners.insert().values(
            name=owner.name,
            email=owner.email,
            hashed_password=hashed_password,
            phone_no=owner.phone_no,
            verified_by=owner.verified_by
        )
        await db.execute(insert_stmt)
        await db.commit()

        return {"message": "User created successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while creating the user. {str(e)}"
        )
