import os
import googlemaps
from fastapi import FastAPI
from datetime import datetime

# 🔹 الحصول على مفتاح API من متغيرات البيئة
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("❌ API Key is missing! Please set API_KEY in Render environment variables.")

gmaps = googlemaps.Client(key=API_KEY)

app = FastAPI()

@app.get("/test_api_key")
def test_api_key():
    return {"API_KEY": API_KEY[:5] + "*****"}  # إظهار جزء صغير للتحقق

@app.get("/get_optimized_route")
def get_optimized_route(origin: str, destination: str):
    try:
        directions = gmaps.directions(
            origin,
            destination,
            mode="driving",
            traffic_model="best_guess",
            departure_time=datetime.now()
        )

        if not directions or "legs" not in directions[0]:
            return {"Error": "No route found or invalid response from Google Maps API", "Response": directions}

        distance_km = directions[0]['legs'][0]['distance']['value'] / 1000
        duration_minutes = directions[0]['legs'][0]['duration_in_traffic']['value'] / 60

        return {
            "Origin": origin,
            "Destination": destination,
            "Distance (km)": round(distance_km, 2),
            "Estimated Travel Time (min)": round(duration_minutes, 2),
            "Raw Response": directions
        }

    except Exception as e:
        return {"Error": "An unexpected error occurred", "Details": str(e)}
