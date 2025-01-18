from fastapi import APIRouter, Form, Depends
from starlette import status
from Services.OwnerSignUp.ownerSignUp import create_owner
from Services.OwnerSignUp.models import OwnerSignUpModel
from sqlalchemy.ext.asyncio import AsyncSession
from Database.Async_DB_Connection import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/signup_owner", status_code=status.HTTP_201_CREATED)
async def signup_owner(
        username: str = Form(...),
        email: str = Form(...),
        phoneNumber = Form(...),
        password: str = Form(...),
        db: AsyncSession = Depends(get_db)
):
    return await create_owner(OwnerSignUpModel(name=username, email=email, phone_no=phoneNumber, password=password), db)

