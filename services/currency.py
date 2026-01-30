import httpx
from core.config import settings

def convert_currency(amount: float, src_currency: str, target_currency: str) -> float:
    """Convert amount from source currency to target currency using external API."""
    response = httpx.get(settings.CURRENCY_API_URL.format(api_key=settings.CURRENCY_API_KEY, base_currency=src_currency, target_currency=target_currency))
    response.raise_for_status()
    exchange_rate = response.json()["data"][target_currency]
    converted_amount = amount * exchange_rate
    return round(converted_amount, 2)