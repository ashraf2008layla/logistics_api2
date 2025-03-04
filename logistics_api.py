import os
import googlemaps
from fastapi import FastAPI
from datetime import datetime

# 🔹 جلب مفتاح API من متغيرات البيئة
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("❌ API Key is missing! Please set API_KEY in Render environment variables.")

gmaps = googlemaps.Client(key=API_KEY)

app = FastAPI()

@app.get("/test_api_key")
def test_api_key():
    return {"API_KEY": API_KEY[:5] + "*****"}  # إظهار جزء صغير فقط للتحقق

@app.get("/get_optimized_route")
def get_optimized_route(origin: str, destination: str):
    directions = gmaps.directions(
        origin,
        destination,
        mode="driving",
        traffic_model="best_guess",
        departure_time=datetime.now()
    )

    if not directions:
        return {"Error": "No route found"}

    distance_km = directions[0]['legs'][0]['distance']['value'] / 1000
    duration_minutes = directions[0]['legs'][0]['duration_in_traffic']['value'] / 60

    return {
        "Origin": origin,
        "Destination": destination,
        "Distance (km)": round(distance_km, 2),
        "Estimated Travel Time (min)": round(duration_minutes, 2)
    }
