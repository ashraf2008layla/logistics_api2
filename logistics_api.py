from fastapi import FastAPI
import googlemaps
import numpy as np
import uvicorn
from datetime import datetime

# استبدل 'YOUR_API_KEY' بمفتاح Google Maps API الخاص بك
API_KEY = "YOUR_API_KEY"
gmaps = googlemaps.Client(key=API_KEY)

# تعريف API
app = FastAPI(title="Smart Logistics API", description="API لحساب المسافات اللوجستية باستخدام Google Maps والطريقة الجديدة", version="3.0")

# دالة جلب المسافات الحية من Google Maps API
def get_real_time_distance(origin, destination):
    try:
        directions = gmaps.directions(
            origin,
            destination,
            mode="driving",  # يدعم المشي، النقل العام، والدراجات أيضًا
            traffic_model="best_guess",  # يأخذ في الاعتبار المرور الحالي
            departure_time=datetime.now()
        )

        if directions:
            distance_km = directions[0]['legs'][0]['distance']['value'] / 1000  # تحويل المسافة إلى كم
            duration_minutes = directions[0]['legs'][0]['duration_in_traffic']['value'] / 60  # الوقت بالدقائق

            return distance_km, duration_minutes
        else:
            return None, None
    except Exception as e:
        return None, None

# دالة الحساب باستخدام المعدل الوسطي مع بيانات Google Maps الحية
def calculate_cost_average_method(distances, traffic_factors):
    avg_distance = np.mean(distances)
    avg_traffic = np.mean(traffic_factors)
    return avg_distance * avg_traffic * len(distances)

@app.get("/get_optimized_route")
def get_optimized_route(origin: str, destination: str):
    real_distance, real_time = get_real_time_distance(origin, destination)

    if real_distance is None:
        return {"Error": "تعذر الحصول على بيانات المسافة من Google Maps"}

    # توليد معاملات ازدحام عشوائية لحين ربط بيانات مرور فعلية
    num_cities_test = 10
    traffic_factors_test = np.random.uniform(1.0, 2.0, size=(num_cities_test, num_cities_test))

    # حساب التكلفة بالطريقة الجديدة
    cost_average_method = calculate_cost_average_method(real_distance, traffic_factors_test)

    return {
        "Method Used": "New Averaging Method",
        "Origin": origin,
        "Destination": destination,
        "Real Distance (km)": real_distance,
        "Estimated Travel Time (min)": real_time,
        "Optimized Cost (km)": cost_average_method
    }

# تشغيل API
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
