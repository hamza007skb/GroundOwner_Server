from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Async_DB_Connection import get_db
from Services.SendRequest.send import AdminNotificationCreate, create_notification

router = APIRouter(
    prefix="/help",
    tags=["Help Request"],
)


@router.post('/')
async def request_help(notification: AdminNotificationCreate, db: AsyncSession = Depends(get_db)):
    await create_notification(notification=notification, db=db)
