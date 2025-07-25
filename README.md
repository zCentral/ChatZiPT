# ChatZiPT
# ChatZiPT@ -1,5 +1,163 @@
# Welcome to GitHub Desktop!
Name: ChatZiPT
Date: 7/25/2025
Time: 4:33pm Dublin Time
## 📈 ZiPT: AI-Powered Trading Signal Engine (Phase 1)

Welcome to **ChatZiPT**, an advanced, modular, and AI-augmented trading assistant system that delivers precision market signals across **forex, metals, crypto, and meme coins**.
This is the **Phase 1 Masterbuild** of the ZiPT system.

---

### 🧠 Core Features

* **Real-Time Pricefeeds**
  Live tracking of **XAUUSD, BTC, ETH**, and meme coins using:

  * Metals-API for XAUUSD
  * Binance and TwelveData for crypto/forex

* **AI Strategy Engine**
  Signal generation using real-time:

  * **Support/Resistance**
  * **MACD**
  * **RSI**
  * **BOLL**
  * **Candlestick Patterns** (Doji, Engulfing, Bullish, Reversal, Pinbar, etc.)
  * **Breakouts, Reversals, and Smart Momentum**
  * **Pattern Detection** (Double Tops, Head & Shoulders, etc.)
  * **Wyckoff & SMC concepts**

* **Confidence Scoring**
  Signals are ranked by AI with accuracy % and logic explanation.
  Only approve sgnals with 90% and above confidence rating.

* **Telegram Bot Integration**

  * Worker bot sends the AI generated signals to channels/groups
  * Manager bot handles commands and system status

* **OpenAI Integration**

  * Custom logic powered by GPT (analysis, summaries, feedback)
  * Codex CLI for inline code transformation

---

### 🧾 File Overview

| Script Name        | Description                                                                |
| ------------------ | -------------------------------------------------------------------------- |
| `zpt_pricefeed.py` | Fetches real-time prices for XAUUSD, BTC, ETH, meme coins                  |
| `zpt_analysis.py`  | Houses TA strategy logic: RSI, MACD, pattern detection, confidence scoring |
| `zipt_worker.py`   | The Telegram bot that dispatches live trading signals                      |
| `zipt_manager.py`  | The master bot for system control, commands, and admin tools               |
| `utils.py`         | Helper functions (symbol mapping, timestamping, currency conversion, etc.) |
| `.env.template`    | Example environment variable template (keys, IDs, configs)                 |

---

### 🧪 Current Supported Strategies

* ✅ RSI / MACD cross-check logic
* ✅ Support and Resistance recognition
* ✅ Candlestick patterns: Doji, Engulfing, Bullish, Reversal, Pinbar
* ✅ Volatility awareness (beta)
* ✅ Breakout + fakeout detection
* ✅ Range vs trend classification
* ✅ AI Reasoning per signal (via GPT)

Planned for Phase 2+:

* 🔜 Trailing SL
* 🔜 Wyckoff phase detection
* 🔜 Smart Money Concepts (SMC)
* 🔜 Multi-timeframe confluence

---

### 🧵 Telegram Integration

Bots are fully integrated via Telegram’s Bot API.
You need:

* `MANAGER_BOT_TOKEN` and `WORKER_BOT_TOKEN`
* Your `ADMIN_ID` (Telegram user ID)
* Target channel/group ID for delivery

The system uses `python-telegram-bot` with async support.

---

### ⚙️ Setup Instructions

1. **Clone the repo**

2. **Create `.env` file** using `.env.template` as a guide

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the bots**

   ```bash
   python zipt_manager.py
   python zipt_worker.py
   ```

5. **Pricefeed (optional standalone)**

   ```bash
   python zpt_pricefeed.py
   ```

---

### 🔑 Environment Variables (.env)

| Key                  | Description                     |
| -------------------- | ------------------------------- |
| `OPENAI_API_KEY`     | my GPT key                    |
| `OPENAI_SERVICE_KEY` | Optional service key (if used)  |
| `METALS_API_KEY`     | XAUUSD feed                     |
| `TELEGRAM_BOT_TOKEN` | Worker bot token                |
| `MANAGER_BOT_TOKEN`  | Manager bot token               |
| `ADMIN_ID`           | Telegram user ID           |
| `CHANNEL_ID`         | Signal destination (group/chat) |

---

### 🧠 Codex CLI

Codex integration allows inline AI edits and suggestions.

```bash
codex explain zpt_analysis.py
codex explain zpt_worker.py
codex explain zpt_manager.py
codex --auto-edit
codex --full-auto
```

> This README helps Codex understand the full repo logic.

---

### 🛠 Paused or Upcoming Features

* [ ] Web app with dashboard
* [ ] Signal freshness tags
* [ ] Confidence-based auto trade trigger
* [ ] Subscription billing (Stripe, Revolut)
* [ ] In-app motivation (e.g. “Take a break” when revenge trading)

---

### 📬 Contact / Credits

Built by Tiffany (ChatZiPT Founder)
Telegram Bot powered by OpenAI Codex + Python Async + JTsu