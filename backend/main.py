from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from services.flights import search_flights
from services.hotels import search_hotels
from services.recommender import get_recommendations

load_dotenv()

app = FastAPI(title="Travel Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TravelRequest(BaseModel):
    origin: str           # "IST"
    destination: str      # "CDG"
    departure_date: str   # "2025-08-01"
    return_date: str      # "2025-08-07"
    adults: int = 1
    category: str         # "budget" | "mid" | "comfort"

@app.get("/")
def root():
    return {"status": "Travel Assistant API çalışıyor"}

@app.post("/search")
async def search(request: TravelRequest):
    try:
        flights = await search_flights(
            request.origin,
            request.destination,
            request.departure_date,
            request.return_date,
            request.adults
        )
        hotels = await search_hotels(
            request.destination,
            request.departure_date,
            request.return_date,
            request.adults
        )
        packages = await get_recommendations(flights, hotels, request.category)
        return packages

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    