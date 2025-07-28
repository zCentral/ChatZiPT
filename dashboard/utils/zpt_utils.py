import os
import logging
from dotenv import load_dotenv
from datetime import datetime
import random

# Error-tolerant loading
try:
    load_dotenv()
except Exception as e:
    print(f"Failed to load .env: {e}")

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "chatzipt.log")),
        logging.StreamHandler()
    ]
)

def get_env(key, default=None):
    val = os.environ.get(key, default)
    if val is None:
        logging.warning(f"{key} not set in environment.")
    return val

def log(msg, level="INFO"):
    getattr(logging, level.lower())(msg)

def safe_float(val):
    try:
        return float(val)
    except Exception:
        return None

def map_symbol(symbol: str) -> str:
    """Normalize symbol to Binance/Bybit format by ensuring it ends with USDT."""
    sym = symbol.upper()
    return sym if sym.endswith("USDT") else f"{sym}USDT"

def health_report() -> dict:
    """Return system health metrics (stub implementation)."""
    return {}

def generate_referral_code(user_id):
    base = f"{user_id}-{random.randint(1000,9999)}"
    return f"REF-{base}"

def get_aura_points(user_data):
    return user_data.get("aura_points", 0)

def pro_features_unlocked(user_data):
    return get_aura_points(user_data) >= 200 or user_data.get("pro_unlock_code_valid", False)