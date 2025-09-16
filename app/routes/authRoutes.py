from fastapi import APIRouter, Depends, HTTPException,Body, Header, Form, status
from datetime import datetime, date
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database.database import get_db, redis_client
from passlib.context import CryptContext
from app.Tables.UserTable import User
from schema import UserCreate, UserLogin, Token
from app.utils.auth import hash_password, verify_password, get_current_user
from sqlalchemy.exc import IntegrityError
from app.utils.jwt import create_access_token, verify_token

router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
    )

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
def register_user(
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    first_user = db.query(User).first()

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.phone_number == user.phone_number).first():
        raise HTTPException(status_code=400, detail="Phone number already registered")
    if db.query(User).filter(User.aadhaar_number == user.aadhaar_number).first():
        raise HTTPException(status_code=400, detail="Aadhaar number already registered")
    
    if user.terms_and_condition_followed == False or user.terms_and_condition_followed == None:
        raise HTTPException(status_code=400, detail="Terms and Condition are required")
    
    hashed_password = hash_password(user.password)
    new_user = User(
        email=user.email,
        full_name= user.full_name,
        password_hash=hashed_password,
        terms_and_condition_followed=user.terms_and_condition_followed,
        phone_number=user.phone_number,
        aadhaar_number=user.aadhaar_number,
        current_village=user.current_village,
        current_taluka=user.current_taluka,
        current_district=user.current_district,
        current_state=user.current_state,
        current_pincode=user.current_pincode,
        total_land_holdings=user.total_land_holdings
    )

    if first_user == None :
        new_user.role = "ADMIN" # type:ignore

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with given details already exists"
        )

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "email": new_user.email,
        "role": new_user.role
    }

@router.post("/login", response_model=Token)
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Authenticate user with phone number and password
    """
    db_user = db.query(User).filter(User.phone_number == user.phone_number and User.email == user.email).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password"
        )
    
    if not db_user.is_active: #type:ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated. Please contact support."
        )
    
    if not verify_password(user.password, db_user.password_hash): #type:ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password"
        )
    
    db_user.last_login = datetime.now() #type:ignore

    access_token = create_access_token(
        data={
            "sub": str(db_user.id),
            "phone": db_user.phone_number,
            "role": db_user.role.value
        }
    )

    db_user.jwt_token = access_token #type:ignore
    db.commit()
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "role": db_user.role.value,
        "full_name": db_user.full_name
    }
    