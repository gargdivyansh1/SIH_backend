from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.utils.auth import get_current_user
from app.Tables.UserTable import User  
from schema import UserProfileOut

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/get_profile/{user_id}", response_model=UserProfileOut)
def get_user(user_id: int, 
             db: Session = Depends(get_db),
           ): 
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    print(user)

    return user
