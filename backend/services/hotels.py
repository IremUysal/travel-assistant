async def search_hotels(destination, check_in, check_out, adults):
    return {
        "hotels": [
            {"name": "Ibis Budget", "stars": 2, "price_per_night": 45, "rating": 7.2},
            {"name": "Novotel", "stars": 4, "price_per_night": 120, "rating": 8.5},
            {"name": "Marriott", "stars": 5, "price_per_night": 280, "rating": 9.1},
            {"name": "Holiday Inn", "stars": 3, "price_per_night": 85, "rating": 7.8},
        ],
        "destination": destination,
        "check_in": check_in,
        "check_out": check_out
    }