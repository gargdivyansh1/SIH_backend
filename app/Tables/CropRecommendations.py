from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base

class CropRecommendation(Base):
    __tablename__ = "crop_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    predicted_crop = Column(String(100), nullable=False)
    suitability_score = Column(String(255))  
    best_planting_time = Column(String(255))
    harvest_period = Column(String(255))
    water_requirements = Column(Text)
    fertilizer_recommendations = Column(Text)
    soil_condition = Column(Text)
    expected_yield = Column(Text) 
    expected_market_price = Column(Text)
    risk_factors = Column(Text) 
    summary = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
