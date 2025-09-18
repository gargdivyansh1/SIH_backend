from datetime import date, datetime
from pydantic import BaseModel, validator, Field, EmailStr
from pydantic import constr, conint, confloat
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

class YieldPredictionRequest(BaseModel):
    Year: int
    average_rain_fall_mm_per_year: float
    pesticides_tonnes: float
    avg_temp: float
    Area: str
    Item: str

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

class IndianState(str, Enum):
    ANDHRA_PRADESH = "Andhra Pradesh"
    ARUNACHAL_PRADESH = "Arunachal Pradesh"
    ASSAM = "Assam"
    BIHAR = "Bihar"
    CHHATTISGARH = "Chhattisgarh"
    GOA = "Goa"
    GUJARAT = "Gujarat"
    HARYANA = "Haryana"
    HIMACHAL_PRADESH = "Himachal Pradesh"
    JHARKHAND = "Jharkhand"
    KARNATAKA = "Karnataka"
    KERALA = "Kerala"
    MADHYA_PRADESH = "Madhya Pradesh"
    MAHARASHTRA = "Maharashtra"
    MANIPUR = "Manipur"
    MEGHALAYA = "Meghalaya"
    MIZORAM = "Mizoram"
    NAGALAND = "Nagaland"
    ODISHA = "Odisha"
    PUNJAB = "Punjab"
    RAJASTHAN = "Rajasthan"
    SIKKIM = "Sikkim"
    TAMIL_NADU = "Tamil Nadu"
    TELANGANA = "Telangana"
    TRIPURA = "Tripura"
    UTTAR_PRADESH = "Uttar Pradesh"
    UTTARAKHAND = "Uttarakhand"
    WEST_BENGAL = "West Bengal"

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

class UserProfileOut(BaseModel):
    id: int
    role: str
    email: str
    terms_and_condition_followed: bool
    phone_number: str
    country_code: Optional[str]
    is_phone_verified: bool
    last_login: Optional[datetime]

    full_name: str
    father_husband_name: Optional[str]
    gender: Optional[str]
    date_of_birth: Optional[datetime]
    profile_photo_url: Optional[str]

    aadhaar_number: Optional[str]
    is_aadhaar_verified: bool
    aadhaar_linked_mobile: bool
    pan_number: Optional[str]
    voter_id: Optional[str]

    current_address: Optional[str]
    current_village: Optional[str]
    current_taluka: Optional[str]
    current_district: Optional[str]
    current_state: Optional[str]
    current_pincode: Optional[str]
    current_gps_lat: Optional[float]
    current_gps_long: Optional[float]

    permanent_address: Optional[str]
    permanent_village: Optional[str]
    permanent_taluka: Optional[str]
    permanent_district: Optional[str]
    permanent_state: Optional[str]
    permanent_pincode: Optional[str]

    total_land_holdings: float
    owned_land_area: float
    leased_land_area: float
    primary_land_type: Optional[str]
    primary_soil_type: Optional[str]
    has_irrigation_facility: bool
    irrigation_type: Optional[str]

    bank_account_number: Optional[str]
    bank_name: Optional[str]
    bank_branch: Optional[str]
    bank_ifsc_code: Optional[str]
    is_bank_verified: bool

    pm_kisan_beneficiary: bool
    pm_kisan_id: Optional[str]
    soil_health_card_id: Optional[str]
    fasal_bima_policy_number: Optional[str]
    kisan_credit_card_number: Optional[str]

    family_members_count: int
    dependents_count: int
    primary_education_level: Optional[str]

    preferred_language: str
    notification_enabled: bool
    sms_alerts_enabled: bool
    voice_call_enabled: bool

    is_active: bool
    is_profile_complete: bool
    profile_completion_percentage: int
    verification_status: str

    created_at: datetime
    updated_at: datetime
    last_profile_update: Optional[datetime]

    class Config:
        orm_mode = True

# class UserLoginResponse(UserBase):
#     id: int
#     role: UserRole
#     access_token: str
#     token_type: str = "bearer"
    
#     class Config:
#         from_attributes = True

# -------- Plant Disease ---------

class_names = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

# -------------- Feedback -----------

class FeedbackCreate(BaseModel):
    rating: int
    category: str
    comment: str

# ---------- Notifications ---------

class NotificationCreate(BaseModel):
    title: str
    message: str
    type: str | None = None

class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    type: str | None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

# ------------- Crop Guidance ----------

class FertilizerData(BaseModel):
    type: Optional[str] = Field(None, example="Urea, DAP") # type:ignore
    amount: Optional[float] = Field(None, example=50.0)  # kg/acre  # type:ignore
    schedule: Optional[str] = Field(None, example="Basal dose at sowing + top dressing 30 days later") # type:ignore

class CropFormRequest(BaseModel):
    crop: str = Field(..., example="Wheat") # type:ignore
    land_size: float = Field(..., example=5.0) # type:ignore
    soil_type: str = Field(..., example="Loamy") # type:ignore
    location: str = Field(..., example="Punjab, India") # type:ignore
    irrigation: str = Field(..., example="Drip") # type:ignore
    fertilizer: Optional[FertilizerData] = None
    equipment: Optional[str] = Field(None, example="Tractor, Plough") # type:ignore
    planting_date: Optional[str] = Field(None, example="2025-10-15") # type:ignore
    growing_season: Optional[str] = Field(None, example="Kharif") # type:ignore

class CropGuidanceResponse(BaseModel):
    guidance: Dict
