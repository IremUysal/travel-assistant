import httpx
import os

async def get_airport_ids(client: httpx.AsyncClient, query: str):
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }
    res = await client.get(
        "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchAirport",
        headers=headers,
        params={"query": query, "locale": "en-US"}
    )
    data = res.json()
    print("AIRPORT API RESPONSE:", data)  # ne döndüğünü göreceğiz
    airport = data["data"][0]
    sky_id = airport["navigation"]["relevantFlightParams"]["skyId"]
    entity_id = airport["navigation"]["relevantFlightParams"]["entityId"]
    return sky_id, entity_id
    

async def search_flights(origin, destination, departure_date, return_date, adults):
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }
    async with httpx.AsyncClient(timeout=30) as client:
        origin_sky_id, origin_entity_id = await get_airport_ids(client, origin)
        dest_sky_id, dest_entity_id = await get_airport_ids(client, destination)

        res = await client.get(
            "https://sky-scrapper.p.rapidapi.com/api/v2/flights/searchFlights",
            headers=headers,
            params={
                "originSkyId": origin_sky_id,
                "destinationSkyId": dest_sky_id,
                "originEntityId": origin_entity_id,
                "destinationEntityId": dest_entity_id,
                "date": departure_date,
                "returnDate": return_date,
                "adults": adults,
                "currency": "EUR",
                "locale": "en-US",
                "market": "TR"
            }
        )
        data= res.json()
        print("FLIGHT API RESPONSE:", str(data)[:500])  # ilk 500 karakter
        return data