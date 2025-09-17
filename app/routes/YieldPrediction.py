from fastapi import FastAPI, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import numpy as np
from dotenv import load_dotenv
import pickle
import sklearn
from schema import YieldPredictionRequest
from geminiResponse import call_gemini_yield
import os
from app.utils.auth import get_current_user
from app.database.database import get_db
from app.Tables.YieldPredictionTable import CropPrediction


load_dotenv()

api_key = os.environ['GEMINI_API_KEY'] 

dtr = pickle.load(open('app/Model/YeildPrediction/dtr.pkl','rb'))
preprocessor = pickle.load(open('app/Model/YeildPrediction/preprocessor.pkl','rb'))

router = APIRouter(
    prefix="/yeild_prediction",
    tags = ['Yeild Prediction']
)


@router.post("/predict")
def predict(
    request: YieldPredictionRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  
):
    features = np.array([[
        request.Year,
        request.average_rain_fall_mm_per_year,
        request.pesticides_tonnes,
        request.avg_temp,
        request.Area,
        request.Item
    ]], dtype=object)

    transformed_features = preprocessor.transform(features)
    prediction = dtr.predict(transformed_features)[0]

    yield_dict = {
        "item": request.Item,
        "area": request.Area,
        "year": request.Year,
        "predicted_yield": round(float(prediction), 2),
        "unit": "hg/ha",
        "rainfall_mm_per_year": request.average_rain_fall_mm_per_year,
        "pesticides_tonnes": request.pesticides_tonnes,
        "avg_temp_celsius": request.avg_temp
    }

    enhanced_response = call_gemini_yield(yield_dict, api_key)

    new_prediction = CropPrediction(
        user_id=current_user.id,   #type:ignore
        item=enhanced_response["item"],
        area=enhanced_response["area"],
        year=enhanced_response["year"],
        predicted_yield=enhanced_response["predicted_yield"],
        unit=enhanced_response["unit"],
        predicted_crop=enhanced_response.get("predicted_crop"),
        suitability_score=enhanced_response.get("suitability_score"),
        best_planting_time=enhanced_response.get("best_planting_time"),
        harvest_period=enhanced_response.get("harvest_period"),
        water_requirements=enhanced_response.get("water_requirements"),
        fertilizer_recommendations=enhanced_response.get("fertilizer_recommendations"),
        soil_condition=enhanced_response.get("soil_condition"),
        expected_yield=enhanced_response.get("expected_yield"),
        expected_market_price=enhanced_response.get("expected_market_price"),
        risk_factors=enhanced_response.get("risk_factors"),
        summary=enhanced_response.get("summary"),
    )

    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    return enhanced_response

