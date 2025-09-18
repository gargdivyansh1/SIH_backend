from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.database import get_db
from app.Tables.Feedbacks import Feedback
from app.utils.auth import get_current_user
from schema import FeedbackCreate
from pydantic import BaseModel

router = APIRouter(
    prefix="/feedbacks",
    tags=['Feedbacks']
)

@router.post("/add_feedback", status_code=status.HTTP_201_CREATED)
def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if feedback.rating < 1 or feedback.rating > 5:
        raise HTTPException(
            status_code=400, detail="Rating must be between 1 and 5."
        )

    new_feedback = Feedback(
        user_id=current_user.id, # type:ignore
        rating=feedback.rating,
        category=feedback.category,
        comment=feedback.comment,
        created_at=datetime.utcnow(),
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    return {"message": "Feedback submitted successfully", "feedback": new_feedback}

@router.get("/my_feedbacks", status_code=status.HTTP_200_OK)
def get_my_feedbacks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    feedbacks = db.query(Feedback).filter(Feedback.user_id == current_user.id).all() #type:ignore

    if not feedbacks:
        return {"message": "No feedbacks found for this user", "feedbacks": []}

    return {"feedbacks": feedbacks}