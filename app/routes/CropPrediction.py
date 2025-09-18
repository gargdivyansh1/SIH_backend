from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session
from schema import CropRequest
import numpy as np
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from geminiResponse import call_gemini
import pickle
from app.database.database import get_db
from app.utils.auth import get_current_user
import json
from app.Tables.CropRecommendations import CropRecommendation

model = pickle.load(open('app/Model/CropPrediction/model.pkl','rb'))
sc = pickle.load(open('app/Model/CropPrediction/standscaler.pkl','rb'))
ms = pickle.load(open('app/Model/CropPrediction/minmaxscaler.pkl','rb'))

load_dotenv()

api_key = os.environ['GEMINI_API_KEY'] 

router = APIRouter(
    prefix="/crop_recommendation",
    tags = ['Crop Recommendation']
)

@router.post("/predict")
def predict(
    request: CropRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  
):
    """
        Endpoint for predicting the best crop according to varoious factors
    """

    N = request.Nitrogen
    P = request.Phosphorus
    K = request.Potassium
    temp = request.Temperature
    humidity = request.Humidity
    ph = request.Ph
    rainfall = request.Rainfall

    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1, -1)

    scaled_features = ms.transform(single_pred)
    final_features = sc.transform(scaled_features)
    prediction = model.predict(final_features)

    crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                 8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                 14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                 19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}
    
    if prediction[0] in crop_dict:
        crop = crop_dict[prediction[0]]
        result = "{} is the best crop to be cultivated right there".format(crop)
    else:
        result = "Sorry, we could not determine the best crop to be cultivated with the provided data."

    CropMidResponse = {
        "Nitrogen": N,
        "Phosphorus": P,
        "Potassium": K,
        "Temperature": temp,
        "Humidity": humidity,
        "Ph": ph,
        "Rainfall": rainfall,
        "crop": crop
    }
    
    response = call_gemini(CropMidResponse, api_key)

    new_recommendation = CropRecommendation(
        user_id=current_user.id, #type:ignore
        predicted_crop=response["predicted_crop"],
        suitability_score=str(response.get("suitability_score")),
        best_planting_time=response.get("best_planting_time"),
        harvest_period=response.get("harvest_period"),
        water_requirements=response.get("water_requirements"),
        fertilizer_recommendations=response.get("fertilizer_recommendations"),
        soil_condition=response.get("soil_condition"),
        expected_yield=response.get("expected_yield"),
        expected_market_price=response.get("expected_market_price"),
        risk_factors=json.dumps(response.get("risk_factors")),  
        summary=response.get("summary"),
    )

    db.add(new_recommendation)
    db.commit()
    db.refresh(new_recommendation)

    return response


@router.get("/recommendations")
def get_user_recommendations(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  
):
    """
    Get all crop recommendations of the logged-in user
    """
    recommendations = db.query(CropRecommendation).filter(
        CropRecommendation.user_id == current_user.id  # type: ignore
    ).all()

    results = []
    for rec in recommendations:
        results.append({
            "id": rec.id,
            "predicted_crop": rec.predicted_crop,
            "suitability_score": rec.suitability_score,
            "best_planting_time": rec.best_planting_time,
            "harvest_period": rec.harvest_period,
            "water_requirements": rec.water_requirements,
            "fertilizer_recommendations": rec.fertilizer_recommendations,
            "soil_condition": rec.soil_condition,
            "expected_yield": rec.expected_yield,
            "expected_market_price": rec.expected_market_price,
            "risk_factors": json.loads(rec.risk_factors) if rec.risk_factors else [], #type:ignore
            "summary": rec.summary,
            "created_at": rec.created_at.isoformat() if rec.created_at else None #type:ignore
        })

    return {"recommendations": results}
