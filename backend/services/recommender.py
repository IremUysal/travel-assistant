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
Sen bir seyahat asistanısın. Aşağıdaki uçuş ve otel verilerine bakarak 
kullanıcıya {category_desc} içeren 3 farklı seyahat paketi öner.

Her paket şunları içermeli:
- Bir uçuş seçeneği (havayolu, fiyat, saat)
- Bir otel seçeneği (otel adı, yıldız, fiyat/gece)
- Toplam tahmini maliyet
- Paketin kısa açıklaması (neden bu paket iyi?)

Yanıtı SADECE JSON formatında ver, başka hiçbir şey yazma:
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
{json.dumps(flights, ensure_ascii=False)[:3000]}

OTEL VERİSİ:
{json.dumps(hotels, ensure_ascii=False)[:3000]}
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)