import requests
import json
from typing import Dict

def call_gemini(crop_data: dict, api_key: str, model: str = "gemini-2.5-flash") -> dict:
    """
    Send crop data to Gemini API and get structured agricultural advice.
    The response will strictly contain all of these keys:
    predicted_crop, suitability_score, best_planting_time, harvest_period,
    water_requirements, fertilizer_recommendations, soil_condition,
    expected_yield, expected_market_price, risk_factors, summary
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    required_keys = [
        "predicted_crop",
        "suitability_score",
        "best_planting_time",
        "harvest_period",
        "water_requirements",
        "fertilizer_recommendations",
        "soil_condition",
        "expected_yield",
        "expected_market_price",
        "risk_factors",
        "summary"
    ]

    instruction = {
        "role": "user",
        "parts": [{
            "text": (
                "You are an agriculture expert. Based on the following crop data, "
                "respond ONLY in valid JSON format with exactly these keys:\n\n"
                f"{required_keys}\n\n"
                f"Crop Data:\n{json.dumps(crop_data)}"
            )
        }]
    }

    body = {
        "contents": [instruction],
        "generationConfig": {
            "response_mime_type": "application/json"
        }
    }

    resp = requests.post(url, headers=headers, json=body)

    if resp.status_code != 200:
        raise Exception(f"Gemini API error {resp.status_code}: {resp.text}")

    data = resp.json()
    try:
        response_text = data["candidates"][0]["content"]["parts"][0]["text"]
        parsed = json.loads(response_text)

        for key in required_keys:
            if key not in parsed:
                parsed[key] = "N/A"

        return parsed

    except Exception:
        return {"error": "Failed to parse Gemini response", "raw": data}
    
def call_gemini_yield(yield_data: dict, api_key: str, model: str = "gemini-2.5-flash") -> Dict:
    """
    Send yield prediction data to Gemini API for enriched agricultural advice.
    The response will strictly contain these keys:
    item, area, year, predicted_yield, unit,
    predicted_crop, suitability_score, best_planting_time, harvest_period,
    water_requirements, fertilizer_recommendations, soil_condition,
    expected_yield, expected_market_price, risk_factors, summary
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    required_keys = [
        "item",
        "area",
        "year",
        "predicted_yield",
        "unit",
        "predicted_crop",
        "suitability_score",
        "best_planting_time",
        "harvest_period",
        "water_requirements",
        "fertilizer_recommendations",
        "soil_condition",
        "expected_yield",
        "expected_market_price",
        "risk_factors",
        "summary"
    ]

    instruction = {
        "role": "user",
        "parts": [{
            "text": (
                "You are an agriculture expert. Based on the following yield prediction data, "
                "respond ONLY in valid JSON format with exactly these keys:\n\n"
                f"{required_keys}\n\n"
                f"Yield Data:\n{json.dumps(yield_data)}"
            )
        }]
    }

    body = {
        "contents": [instruction],
        "generationConfig": {
            "response_mime_type": "application/json"
        }
    }

    resp = requests.post(url, headers=headers, json=body)

    if resp.status_code != 200:
        raise Exception(f"Gemini API error {resp.status_code}: {resp.text}")

    data = resp.json()
    try:
        response_text = data["candidates"][0]["content"]["parts"][0]["text"]
        parsed = json.loads(response_text)

        for key in required_keys:
            if key not in parsed:
                parsed[key] = "N/A"

        return parsed

    except Exception:
        return {"error": "Failed to parse Gemini response", "raw": data}