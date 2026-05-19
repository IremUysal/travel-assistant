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
Sen bir seyahat asistanısın. Aşağıdaki uçuş ve otel verilerini kullanarak kullanıcıya {category_desc} içeren 3 farklı seyahat paketi öner.

UÇUŞ VERİSİ:
{json.dumps(flights.get("itineraries", []), ensure_ascii=False)}

OTEL VERİSİ:
{json.dumps(hotels.get("hotels", []), ensure_ascii=False)}

Bu verilerden {category_desc} seç ve 3 paket oluştur. Her pakette bir uçuş ve bir otel olmalı.

SADECE şu JSON formatında yanıt ver, başka hiçbir şey yazma:
{{
  "packages": [
    {{
      "id": 1,
      "title": "Paket adı",
      "description": "Bu paketi neden seçmeli, 1-2 cümle",
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