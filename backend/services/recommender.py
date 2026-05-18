import os
import json
from dotenv import load_dotenv

load_dotenv()

CATEGORY_MAP = {
    "budget": "en ucuz seçenekleri",
    "mid": "fiyat/performans dengesi en iyi seçenekleri",
    "comfort": "en konforlu ve kaliteli seçenekleri"
}

async def get_recommendations(flights: dict, hotels: dict, category: str):
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    category_desc = CATEGORY_MAP.get(category, "en uygun seçenekleri")

    prompt = f"""
Sen bir JSON tabanlı travel recommendation engine'sin.
ÖNEMLİ KURALLAR:
- SADECE verilen uçuş ve otel verilerini kullan
- Yeni uçuş veya otel uydurma
- Her pakette MUTLAKA bir flight ve bir hotel olmalı
- Flight bilgileri MUTLAKA input flights JSON'undan seçilmeli
- Hotel bilgileri MUTLAKA input hotels JSON'undan seçilmeli
- Eğer veri eksikse hata mesajı döndür
- Generic açıklamalar yazma
- Her pakette airline, departure, arrival ve hotel name alanları dolu olmalı
- SADECE geçerli JSON döndür
ÖRNEK:

Input flight:
{
  "airline": "Turkish Airlines",
  "price": 189
}

Input hotel:
{
  "name": "Hilton Paris",
  "price_per_night": 120
}

Expected output:
{
  "flight": {
    "airline": "Turkish Airlines",
    "price": 189
  },
  "hotel": {
    "name": "Hilton Paris",
    "price_per_night": 120
  }
}

{{
  "packages": [
    {{
      "id": 1,
      "title": "Paket adı",
      "description": "Kısa açıklama",
      "flight": {{
        "airline": "Havayolu adı",
        "departure": "Kalkış saati",
        "arrival": "Varış saati",
        "price": 000
      }},
      "hotel": {{
        "name": "Otel adı",
        "stars": 4,
        "price_per_night": 000
      }},
      "total_price": 000
    }}
  ]
}}

UÇUŞ VERİSİ:
{json.dumps(flights.get("itineraries", []), ensure_ascii=False)}

OTEL VERİSİ:
{json.dumps(hotels.get("hotels", []), ensure_ascii=False)}
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    # Tüm content bloklarına bak
    raw = ""
    for block in message.content:
        if hasattr(block, 'text'):
            raw += block.text

    # JSON'u bul ve parse et
    import re
    json_match = re.search(r'\{.*\}', raw, re.DOTALL)
    if json_match:
        clean = json_match.group()
        return json.loads(clean)
    else:
        raise ValueError(f"JSON bulunamadi. Raw: {raw[:500]}")