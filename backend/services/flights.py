async def search_flights(origin, destination, departure_date, return_date, adults):
    return {
        "itineraries": [
            {"airline": "Turkish Airlines", "price": 189, "departure": f"{departure_date}T06:30", "arrival": f"{departure_date}T09:15", "stops": 0},
            {"airline": "Pegasus", "price": 134, "departure": f"{departure_date}T11:00", "arrival": f"{departure_date}T13:45", "stops": 0},
            {"airline": "Lufthansa", "price": 320, "departure": f"{departure_date}T16:00", "arrival": f"{departure_date}T19:30", "stops": 1},
            {"airline": "Qatar Airways", "price": 450, "departure": f"{departure_date}T22:00", "arrival": f"{departure_date}T08:00", "stops": 1},
        ],
        "origin": origin,
        "destination": destination,
        "date": departure_date
    }