from select import select

from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from Database.async_tables import get_admin_notifications_table


class AdminNotificationCreate(BaseModel):
    subject: str
    body: str


async def send_help(notification: AdminNotificationCreate, db: AsyncSession):
    try:
        admin_notifications_table = await get_admin_notifications_table()
        stmt = insert(admin_notifications_table).values(subject=notification.subject, body=notification.body)
        await db.execute(stmt)
        await db.commit()  # Commit the transaction

        return {"message": "Notification sent successfully!"}

    except Exception as e:
        await db.rollback()  # Rollback in case of an error
        return {"error": str(e)}
