from fastapi import FastAPI, APIRouter
from schema import CropRequest
import numpy as np
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from geminiResponse import call_gemini
import pickle

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
def predict(request: CropRequest):
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
    
    json_response = call_gemini(CropMidResponse, api_key)

    return json_response
