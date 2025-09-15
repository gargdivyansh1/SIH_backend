from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, Float, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base
import enum

class UserRole(enum.Enum):
    FARMER = "farmer"
    EXPERT = "expert"
    ADMIN = "admin"

class LandType(enum.Enum):
    IRRIGATED = "irrigated"
    RAINFED = "rainfed"
    SEMI_IRRIGATED = "semi_irrigated"
    HORTICULTURE = "horticulture"
    ORCHARD = "orchard"

class SoilType(enum.Enum):
    ALLUVIAL = "alluvial"
    BLACK = "black"
    RED = "red"
    LATERITE = "laterite"
    MOUNTAIN = "mountain"
    DESERT = "desert"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role = Column(Enum(UserRole))
    email = Column(String, unique=True, index=True, nullable=False)
    terms_and_condition_followed = Column(Boolean, nullable=False)
    
    phone_number = Column(String(15), unique=True, index=True, nullable=False)
    country_code = Column(String(5), default="+91")
    password_hash = Column(String(255), nullable=False)
    is_phone_verified = Column(Boolean, default=False)
    otp_secret = Column(String(255))  
    last_login = Column(DateTime(timezone=True))

    full_name = Column(String(255), nullable=False)
    father_husband_name = Column(String(255)) 
    gender = Column(Enum('male', 'female', 'other', name='gender_enum'))
    date_of_birth = Column(DateTime)
    profile_photo_url = Column(String(500))

    aadhaar_number = Column(String(12), unique=True, index=True)
    is_aadhaar_verified = Column(Boolean, default=False)
    aadhaar_linked_mobile = Column(Boolean, default=False)
    pan_number = Column(String(10), unique=True)
    voter_id = Column(String(20))

    current_address = Column(Text)
    current_village = Column(String(100))
    current_taluka = Column(String(100))
    current_district = Column(String(100))
    current_state = Column(String(100))
    current_pincode = Column(String(10))
    current_gps_lat = Column(Float)
    current_gps_long = Column(Float)

    permanent_address = Column(Text)
    permanent_village = Column(String(100))
    permanent_taluka = Column(String(100))
    permanent_district = Column(String(100))
    permanent_state = Column(String(100))
    permanent_pincode = Column(String(10))

    total_land_holdings = Column(Float, default=0.0)  # in acres/hectares
    owned_land_area = Column(Float, default=0.0)
    leased_land_area = Column(Float, default=0.0)
    primary_land_type = Column(Enum(LandType))
    primary_soil_type = Column(Enum(SoilType))
    has_irrigation_facility = Column(Boolean, default=False)
    irrigation_type = Column(String(100))  # borewell, canal, well, etc.

    bank_account_number = Column(String(50))
    bank_name = Column(String(100))
    bank_branch = Column(String(100))
    bank_ifsc_code = Column(String(20))
    is_bank_verified = Column(Boolean, default=False)

    pm_kisan_beneficiary = Column(Boolean, default=False)
    pm_kisan_id = Column(String(50))
    soil_health_card_id = Column(String(50))
    fasal_bima_policy_number = Column(String(50))
    kisan_credit_card_number = Column(String(50))

    family_members_count = Column(Integer, default=0)
    dependents_count = Column(Integer, default=0)
    primary_education_level = Column(String(50))  # illiterate, primary, secondary, graduate

    preferred_language = Column(String(10), default='hi')  # hi, en, te, mr, etc.
    notification_enabled = Column(Boolean, default=True)
    sms_alerts_enabled = Column(Boolean, default=True)
    voice_call_enabled = Column(Boolean, default=True)

    role = Column(Enum(UserRole), default=UserRole.FARMER)
    is_active = Column(Boolean, default=True)
    is_profile_complete = Column(Boolean, default=False)
    profile_completion_percentage = Column(Integer, default=0)
    verification_status = Column(String(50), default='pending')  # pending, verified, rejected

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_profile_update = Column(DateTime(timezone=True))
