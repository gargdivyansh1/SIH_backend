from sqlalchemy import Column, Integer, BigInteger, String, Float, DateTime, Date, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from app.database.database import Base

class CropGuidances(Base):
    __tablename__ = "crop_guidance_table"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=True, index=True) 
    crop_name = Column(String(100), nullable=False)
    land_size = Column(Float, nullable=False)
    soil_type = Column(String(50), nullable=False)
    location = Column(String(100), nullable=False)
    irrigation_method = Column(String(50), nullable=False)
    fertilizer = Column(JSONB, nullable=True)  # Fertilizer details
    equipment = Column(String(200), nullable=True)
    planting_date = Column(Date, nullable=True)
    growing_season = Column(String(50), nullable=True)
    guidance_response = Column(JSONB, nullable=False)  # Full detailed Gemini output
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
