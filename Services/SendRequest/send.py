from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert
from datetime import datetime
from pydantic import BaseModel
from Database.async_tables import get_admin_notifications_table

class AdminNotificationCreate(BaseModel):
    subject: str
    body: str

async def create_notification(
    notification: AdminNotificationCreate, db: AsyncSession
):
    try:
        # Reflect the admin_notifications table
        admin_notifications_table = await get_admin_notifications_table()

        # Insert the new notification
        query = insert(admin_notifications_table).values(
            subject=notification.subject,
            body=notification.body,
            created_at=datetime.utcnow(),
            read=False
        )
        await db.execute(query)
        await db.commit()
        return {"message": "Notification created successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
