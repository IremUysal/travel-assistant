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
   from_location: str    # "Istanbul"
   to: str              # "Paris"
   date: str            # "2025-08-01"
   return_date: str = "" # opsiyonel
   passengers: int = 1
   category: str        # "budget" | "mid" | "comfort"

@app.get("/")
def root():
    return {"status": "Travel Assistant API çalışıyor"}

@app.post("/search")
async def search(request: TravelRequest):
    try:
        flights = await search_flights(
            request.from_location,
            request.to,
            request.date,
            request.return_date or request.date,
            request.passengers
        )
        hotels = await search_hotels(
            request.to,
            request.date,
            request.return_date or request.date,
            request.passengers
        )
        packages = await get_recommendations(flights, hotels, request.category)
        return packages
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    