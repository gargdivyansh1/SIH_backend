from fastapi import APIRouter, HTTPException, Depends
from schema import CropGuidanceResponse, CropFormRequest
from dotenv import load_dotenv
import os
from geminiResponse import call_gemini_for_guidance
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.Tables.CropGuidance import CropGuidances
from app.Tables.UserTable import User
from app.utils.auth import get_current_user

load_dotenv()

api_key = os.environ['GEMINI_API_KEY']

router = APIRouter(
    prefix="/crop_guidance",
    tags=["Crops Guidance"]
)

@router.post("/getting_guidance")
def give_guidance(
    crop_data: CropFormRequest, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Accepts crop form data, calls Gemini API, stores the response, 
    and returns ultra-detailed crop guidance.
    """
    try:
        guidance = call_gemini_for_guidance(crop_data, api_key=api_key)

        db_entry = CropGuidances(
            user_id=current_user.id, #type:ignore
            crop_name=crop_data.crop,
            land_size=crop_data.land_size, #type:ignore
            soil_type=crop_data.soil_type,  #type:ignore
            location=crop_data.location,
            irrigation_method=crop_data.irrigation,
            fertilizer={
                "type": crop_data.fertilizer.type,  #type:ignore
                "amount": crop_data.fertilizer.amount,  #type:ignore
                "schedule": crop_data.fertilizer.schedule  #type:ignore
            },
            equipment=crop_data.equipment, 
            planting_date=crop_data.planting_date or None, #type:ignore
            growing_season=crop_data.growing_season,  #type:ignore
            guidance_response=guidance
        )
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)

        from fastapi.responses import JSONResponse
        return JSONResponse(content={"guidance": guidance})

    except Exception as e:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"detail": str(e)})

@router.get("/user_guidance")
def getting_guidance(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Getting the guidances which a specific user has taken"""

    guidances = db.query(CropGuidances).filter(
        CropGuidances.user_id == current_user.id #type:ignore
    ).all()

    if not guidances:
        return []
        
    return guidances

