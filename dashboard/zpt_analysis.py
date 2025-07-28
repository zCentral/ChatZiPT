import pandas as pd
import requests
import ta
import openai
from utils import (
    get_env,
    log,
    map_symbol,
    safe_float,
    health_report,
    get_aura_points,
    pro_features_unlocked,
    generate_sn,
)
from zpt_pricefeed import get_price, get_new_bybit_coins

openai.api_key = get_env("OPENAI_API_KEY")

def fetch_ohlc_binance(symbol: str, interval: str = "1h", limit: int = 100) -> pd.DataFrame:
    url = f"https://api.binance.com/api/v3/klines?symbol={map_symbol(symbol)}&interval={interval}&limit={limit}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        df = pd.DataFrame(data, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "qav", "num_trades", "taker_base_vol", "taker_quote_vol", "ignore"
        ])
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    except Exception as e:
        log(f"OHLC fetch error: {e}", level="ERROR")
        return pd.DataFrame()

def multi_timeframe_confluence(symbol: str) -> dict:
    timeframes = ["15m", "1h", "4h"]
    results = {}
    for tf in timeframes:
        df = fetch_ohlc_binance(symbol, interval=tf, limit=100)
        action, conf = ta_signal(df) if not df.empty else ("HOLD", 0.5)
        results[tf] = {"action": action, "confidence": conf}
    actions = [r["action"] for r in results.values()]
    final = max(set(actions), key=actions.count)
    avg_conf = sum([r["confidence"] for r in results.values()]) / len(results)
    return {"action": final, "confidence": avg_conf, "details": results}

def ta_signal(df: pd.DataFrame) -> tuple[str, float]:
    if df.empty:
        return "HOLD", 0.5
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    macd = ta.trend.MACD(df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["bb_width"] = ta.volatility.BollingerBands(df["close"]).bollinger_wband()
    last = df.iloc[-1]
    wick_size = last["high"] - last["close"]
    smc_signal = "LONG" if wick_size > last["close"] * 0.01 else "SHORT" if wick_size < -last["close"] * 0.01 else "HOLD"
    wyckoff_signal = "LONG" if last["volume"] > df["volume"].mean() * 1.5 else "HOLD"
    candle_signal = "HOLD"
    if (last["close"] > last["open"] and (last["low"] < last["open"] * 0.99)):
        candle_signal = "LONG"
    votes = [smc_signal, wyckoff_signal, candle_signal]
    final_action = max(set(votes), key=votes.count)
    confidence = 0.90 if final_action != "HOLD" else 0.80
    if last["rsi"] < 30 and last["macd"] > last["macd_signal"]:
        final_action = "LONG"
        confidence += 0.05
    elif last["rsi"] > 70 and last["macd"] < last["macd_signal"]:
        final_action = "SHORT"
        confidence += 0.05
    confidence = min(confidence, 0.99)
    return final_action, confidence

def sl_tp_logic(df, confidence):
    if df.empty:
        return {"SL": None, "TP": []}
    latest = df.iloc[-1]
    volatility = df["high"].std()
    sl = latest["close"] - volatility
    tp = []
    if confidence < 0.9:
        tp = [latest["close"] + volatility * i for i in range(1, 4)]
    else:
        tp = [latest["close"] + volatility * i for i in range(1, 7)]
    return {"SL": round(sl,2), "TP": [round(x,2) for x in tp]}


def ai_explain(symbol: str, action: str, price: float, confidence: float) -> str:
    prompt = (
        f"Asset: {symbol}, Price: {price}, Signal: {action}, Confidence: {int(confidence*100)}%.\n"
        f"Explain in plain English the technical and AI logic behind this signal, referencing multi-timeframe, SMC, Wyckoff, and candle analysis. "
        f"Keep it concise but informative for traders."
    )
    try:
        # Updated to use new OpenAI client
        import openai
        client = openai.OpenAI(api_key=get_env("OPENAI_API_KEY"))
        
        resp = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        log(f"OpenAI error: {e}", level="ERROR")
        return "AI explanation unavailable."

def analyze(symbol: str = "BTCUSDT", user_data=None) -> dict:
    mtf = multi_timeframe_confluence(symbol)
    price = get_price(symbol)
    explanation = ai_explain(symbol, mtf["action"], price, mtf["confidence"])
    df = fetch_ohlc_binance(symbol)
    sltp = sl_tp_logic(df, mtf["confidence"])
    sn = generate_sn(symbol)
    aura_points = get_aura_points(user_data or {})
    pro_unlocked = pro_features_unlocked(user_data or {})
    return {
        "symbol": symbol,
        "action": mtf["action"],
        "confidence": mtf["confidence"],
        "price": price,
        "details": mtf["details"],
        "explanation": explanation,
        "SLTP": sltp,
        "SN": sn,
        "aura_points": aura_points,
        "pro_unlocked": pro_unlocked
    }

def vibe_response(user_vibe, trade_signal):
    if user_vibe == "revenge":
        return "Let's take a step back. Revenge trades rarely work out. Review your last signals and wait for a high-confidence setup."
    elif user_vibe == "anxious":
        return "Stay calm. Risk management is your friend. Let's focus on signals with top confidence today."
    elif user_vibe == "confident":
        return "Great energy! Stick to your lot cap and keep emotions in check. Let's go!"
    else:
        return "I'm here to guide you with balanced signals. Ask me for explanations anytime!"

def meme_shitcoin_analysis(user_data=None):
    """Analyze meme/shitcoins, filter for 90%+ confidence, short/long-term."""
    coins = ["DOGEUSDT", "SHIBUSDT", "PEPEUSDT"]
    # Add new Bybit coins
    new_bybit_coins = get_new_bybit_coins()
    coins += [c for c in new_bybit_coins if c not in coins]
    results = []
    for coin in coins:
        res = analyze(coin, user_data)
        # Only include ultra-high-confidence signals (95.5%+)
        if res["confidence"] >= 0.955:
            res["trend"] = "long-term" if res["action"] == "LONG" else "short-term" if res["action"] == "SHORT" else "hold"
            results.append(res)
    return results

if __name__ == "__main__":
    print("Meme/Shitcoin analysis:")
    for r in meme_shitcoin_analysis({"aura_points": 200, "pro_unlock_code_valid": True}):
        print(r)