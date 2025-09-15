from datetime import date, datetime
from pydantic import BaseModel, validator, Field, EmailStr
from typing import Dict, List, Optional
from enum import Enum

# -------- ChatBot -----------
class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str
    stream: bool = True

class ChatResponse(BaseModel):
    reponse: str

class ChatMessage(BaseModel):
    role: str
    content: str

# -------- Yeild Prediciton ----------
class CropYieldRequest(BaseModel):
    """Request model for crop yield prediction"""
    crop: str = Field(..., description="Type of crop")
    season: str = Field(..., description="Growing season")
    state: str = Field(..., description="State/region")
    annual_rainfall: float = Field(..., ge=0, le=10000, description="Annual rainfall in mm")
    pesticide: float = Field(..., ge=0, le=100000, description="Pesticide usage")
    
    @validator('crop')
    def validate_crop(cls, v):
        return v.strip()
    
    @validator('season')
    def validate_season(cls, v):
        return v.strip()
    
    @validator('state')
    def validate_state(cls, v):
        return v.strip()
    
class CropYieldResponse(BaseModel):
    """Response model for crop yield prediction"""
    predicted_yield: float = Field(..., description="Predicted crop yield")
    confidence_score: float = Field(..., description="Model confidence (R² score)")
    input_summary: Dict = Field(..., description="Summary of input parameters")

# ------------ Crop Recommendation ---------

class CropRequest(BaseModel):
    """Crop Recommendation form data"""
    Nitrogen: float
    Phosphorus: float
    Potassium: float
    Temperature: float
    Humidity: float
    Ph: float
    Rainfall: float

# ---------- User Create ---------------

class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class LandType(str, Enum):
    AGRICULTURAL = "agricultural"
    NON_AGRICULTURAL = "non_agricultural"

class SoilType(str, Enum):
    CLAY = "clay"
    SANDY = "sandy"
    LOAMY = "loamy"

class UserRole(str, Enum):
    FARMER = "farmer"
    EXPERT = "expert"
    ADMIN = "admin"

# class IndianState(str, Enum):
#     ANDHRA_PRADESH = "Andhra Pradesh"
#     ARUNACHAL_PRADESH = "Arunachal Pradesh"
#     ASSAM = "Assam"
#     BIHAR = "Bihar"
#     CHHATTISGARH = "Chhattisgarh"
#     GOA = "Goa"
#     GUJARAT = "Gujarat"
#     HARYANA = "Haryana"
#     HIMACHAL_PRADESH = "Himachal Pradesh"
#     JHARKHAND = "Jharkhand"
#     KARNATAKA = "Karnataka"
#     KERALA = "Kerala"
#     MADHYA_PRADESH = "Madhya Pradesh"
#     MAHARASHTRA = "Maharashtra"
#     MANIPUR = "Manipur"
#     MEGHALAYA = "Meghalaya"
#     MIZORAM = "Mizoram"
#     NAGALAND = "Nagaland"
#     ODISHA = "Odisha"
#     PUNJAB = "Punjab"
#     RAJASTHAN = "Rajasthan"
#     SIKKIM = "Sikkim"
#     TAMIL_NADU = "Tamil Nadu"
#     TELANGANA = "Telangana"
#     TRIPURA = "Tripura"
#     UTTAR_PRADESH = "Uttar Pradesh"
#     UTTARAKHAND = "Uttarakhand"
#     WEST_BENGAL = "West Bengal"

class UserBase(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=15)
    country_code: str = Field(default="+91")
    email: EmailStr
    role: UserRole = UserRole.FARMER

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    confirm_password: str
    full_name: str 
    terms_and_condition_followed: bool
    aadhaar_number: str = Field(..., min_length=12, max_length=12)
    current_village: str = Field(..., max_length=100)
    current_taluka: str = Field(..., max_length=100)
    current_district: str = Field(..., max_length=100)
    current_state: str
    current_pincode: str = Field(..., max_length=6, min_length=6)
    
    total_land_holdings: float = Field(..., ge=0.0)

    primary_land_type: Optional[LandType] = LandType.AGRICULTURAL
    primary_soil_type: Optional[SoilType] = SoilType.LOAMY
    preferred_language: Optional[str] = Field(default='hi', max_length=10)
    is_phone_verified: Optional[bool] = False
    otp_secret: Optional[str] = None
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        if not v.isdigit():
            raise ValueError('Phone number must contain only digits')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v
    
    @validator("confirm_password")
    def validate_confirm_password(cls, v, values):
        password = values.get("password")
        if password and v != password:
            raise ValueError("Passwords do not match")
        return v
    
class UserLogin(BaseModel):
    password: str = Field(..., min_length=6)
    phone_number: str = Field(..., min_length=10, max_length=15)
    email: EmailStr
    country_code: Optional[str] = Field(default="+91")
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        if not v.isdigit():
            raise ValueError('Phone number must contain only digits')
        return v

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: str
    full_name: str

# class UserLoginResponse(UserBase):
#     id: int
#     role: UserRole
#     access_token: str
#     token_type: str = "bearer"
    
#     class Config:
#         from_attributes = True
