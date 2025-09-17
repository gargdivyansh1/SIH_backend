from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base

class CropPrediction(Base):
    __tablename__ = "crop_predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    item = Column(String(100), nullable=False)  
    area = Column(String(100), nullable=False) 
    year = Column(Integer, nullable=False)

    predicted_yield = Column(Integer, nullable=False)  
    unit = Column(String(20), nullable=False, default="hg/ha")
    predicted_crop = Column(String(100), nullable=False)

    suitability_score = Column(String(255))  
    best_planting_time = Column(String(255))
    harvest_period = Column(String(255))
    water_requirements = Column(Text)
    fertilizer_recommendations = Column(Text)
    soil_condition = Column(Text)

    expected_yield = Column(Text, nullable=True)
    expected_market_price = Column(Text)  
    risk_factors = Column(Text)

    summary = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())