from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.Tables.Notiifcaitions import Notification
from app.utils.auth import get_current_user
from pydantic import BaseModel
from datetime import datetime
from schema import NotificationCreate, NotificationResponse

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.post("/create", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_notification = Notification(
        user_id=current_user.id,  # type: ignore
        title=notification.title,
        message=notification.message,
        type=notification.type,
        is_read=False
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    return new_notification


@router.get("/my_notifications", response_model=List[NotificationResponse])
def get_my_notifications(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id) #type:ignore
        .order_by(Notification.created_at.desc())
        .all()
    )
    return notifications


@router.put("/mark_as_read/{notification_id}", response_model=NotificationResponse)
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.user_id == current_user.id) #type:ignore
        .first()
    )

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True #type:ignore
    db.commit()
    db.refresh(notification)

    return notification


@router.delete("/delete/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.user_id == current_user.id) #type:ignore
        .first()
    )

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    db.delete(notification)
    db.commit()

    return {"message": "Notification deleted successfully"}
