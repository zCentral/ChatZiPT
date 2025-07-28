import requests
from utils import get_env, map_symbol, log, safe_float, health_report
from typing import Optional

def get_xauusd_metalsapi() -> Optional[float]:
    api_key = get_env("METALS_API_KEY")
    if not api_key:
        log("METALS_API_KEY not set in environment.", level="ERROR")
        return None
    # Use MetalPriceAPI endpoint for latest rates (free plan supports timeseries only)
    url = (
        f"https://api.metalpriceapi.com/v1/latest"
        f"?api_key={api_key}"
        f"&base=USD"
        f"&currencies=XAU"
    )
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        # Handle invalid key or API error
        if data.get("status") == "error" or data.get("error"):
            err = data.get("error") or data.get("message") or data.get("info")
            log(f"Metals API error: {err}", level="ERROR")
            return None
        rate = data.get("rates", {}).get("XAU")
        if rate is None:
            log("Metals API: XAU rate missing in response.", level="ERROR")
            return None
        # 'rate' is ounces per USD; invert to get USD per ounce
        price = 1 / rate
        return round(price, 2)
    except Exception as e:
        log(f"Metals API error: {e}", level="ERROR")
        return None

def get_crypto_binance(symbol: str) -> Optional[float]:
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={map_symbol(symbol)}"
    try:
        resp = requests.get(url, timeout=10)
        return safe_float(resp.json()["price"])
    except Exception as e:
        log(f"Binance error: {e}", level="WARNING")
        return None

def get_crypto_bybit(symbol: str) -> Optional[float]:
    url = f"https://api.bybit.com/v5/market/tickers?category=linear&symbol={map_symbol(symbol)}"
    try:
        resp = requests.get(url, timeout=10)
        tickers = resp.json().get("result", {}).get("list", [])
        if tickers:
            return safe_float(tickers[0]["lastPrice"])
    except Exception as e:
        log(f"Bybit error: {e}", level="WARNING")
    return None

def get_price(symbol: str) -> Optional[float]:
    symbol = symbol.upper()
    if symbol == "XAUUSD":
        return get_xauusd_metalsapi()
    for fetcher in [get_crypto_binance, get_crypto_bybit]:
        price = fetcher(symbol)
        if price is not None:
            return price
    log(f"Failed to fetch price for {symbol}", level="ERROR")
    return None

def get_new_bybit_coins():
    """Fetch new coins from Bybit API (spot/linear/futures)."""
    url = f"https://api.bybit.com/v5/market/tickers?category=spot"
    try:
        resp = requests.get(url, timeout=10)
        coins = resp.json().get("result", {}).get("list", [])
        new_coins = [c for c in coins if c.get("listTime") and int(c["listTime"]) > 1680000000000]  # Example: filter listed after a certain timestamp
        return [c["symbol"] for c in new_coins]
    except Exception as e:
        log(f"Bybit new coins error: {e}", level="WARNING")
        return []

def price_health():
    """Expose health status to other modules/bots."""
    core_assets = ["XAUUSD", "BTC", "ETH", "DOGE", "SHIB", "PEPE"]
    status = {asset: get_price(asset) for asset in core_assets}
    status.update(health_report())
    return status

if __name__ == "__main__":
    for asset in ["XAUUSD", "BTC", "ETH", "DOGE", "SHIB", "PEPE"]:
        price = get_price(asset)
        log(f"{asset} price: {price}")
    log(f"New Bybit coins: {get_new_bybit_coins()}")