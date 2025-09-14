from pydantic import BaseModel, validator, Field
from typing import Dict, List

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

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    model_loaded: bool

class ModelInfoResponse(BaseModel):
    """Model information response"""
    model_type: str
    features_count: int
    available_crops: List[str]
    available_seasons: List[str]
    available_states: List[str]

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

