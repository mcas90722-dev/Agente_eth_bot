import os
import yfinance as yf
from google import genai
import requests

# 1. Obtener datos de Ethereum
data = yf.download("ETH-USD", period="5d", interval="1d")
precio_actual = data["Close"].iloc[-1].item()

# 2. Prompt con el reporte técnico y el veredicto operativo obligatorio
prompt = f"""
Analiza el precio actual de Ethereum (ETH-USD) que es {precio_actual}. 
Proporciona un reporte técnico corto para trading que incluya:
- Tendencia actual.
- Niveles clave de soporte y resistencia.
- AL FINAL, añade obligatoriamente un apartado titulado "VEREDICTO OPERATIVO" donde indiques claramente si las condiciones sugieren: **COMPRAR**, **VENDER** o **ESPERAR**.
"""

# 3. Consultar a Gemini usando la librería oficial google-genai
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt
)
analisis = response.text

# 4. Enviar a Telegram
token = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("CHAT_ID")
url = f"https://api.telegram.org/bot{token}/sendMessage"

payload = {
    "chat_id": chat_id,
    "text": f"💎 **Reporte Ethereum (ETH/USD)**\n\n{analisis}",
    "parse_mode": "Markdown"
}
requests.post(url, json=payload)
