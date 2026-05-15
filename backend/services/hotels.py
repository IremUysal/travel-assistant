import httpx
import os

async def search_hotels(destination, check_in, check_out, adults):
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }
    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.get(
            "https://sky-scrapper.p.rapidapi.com/api/v1/hotels/searchHotels",
            headers=headers,
            params={
                "query": destination,
                "checkIn": check_in,
                "checkOut": check_out,
                "adults": adults,
                "currency": "EUR",
                "locale": "en-US"
            }
        )
        return res.json()