import requests
from django.conf import settings

def get_gemini_price(symbol):
    url = f"{settings.GEMINI_API_BASE_URL}/pubticker/{symbol}"
    try:
        response = requests.get(url, auth=(settings.GEMINI_API_KEY, settings.GEMINI_API_SECRET))
        response.raise_for_status()
        data = response.json()
        return data['last']
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching data from Gemini API: {e}")
