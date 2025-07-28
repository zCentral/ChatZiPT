# ChatZiPT v4 Dashboard

A self-hosted Streamlit UI and Telegram bots for ChatZiPT v4, an AI-powered trading assistant.

---

## 🔥 Features

- Live pricefeeds for XAUUSD, BTC, ETH via Metals-API, Binance & Bybit
- AI-driven trading signals with confidence scoring & reasoning
- Telegram Manager & Worker Bots for natural language queries & signals
- Single-file Streamlit UI: `dashboard.py`
- Performance monitoring & logging

---

## 🚀 Quick Start

```bash
git clone <YOUR_REPO_URL>
cd ChatZiPT/dashboard
```

### 1. Create & activate a Python virtual environment

```bash
python3 -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
# Windows CMD
.venv\\Scripts\\activate.bat
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root and add **your own** API keys/tokens. Example:

```dotenv
# OpenAI (optional)
OPENAI_API_KEY=<your OpenAI API key>

# Market data
METALS_API_KEY=<your Metals-API key>
BINANCE_API_KEY=<your Binance API key>
BINANCE_API_SECRET=<your Binance API secret>
BYBIT_API_KEY=<your Bybit API key>
BYBIT_API_SECRET=<your Bybit API secret>

# Telegram bots & admin
MANAGER_BOT_TOKEN=<your manager bot token>
TELEGRAM_BOT_TOKEN=<your worker bot token>
ADMIN_ID=<your Telegram user ID>
CHANNEL_ID=<your Telegram channel/group ID>
```

### 4. (Optional) Streamlit server config

To serve on all interfaces or customize port, create `.streamlit/config.toml`:

```toml
[server]
address = "0.0.0.0"
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = false
```

### 5. Run the dashboard & bots

#### Automated (Windows CMD)

Ensure your virtual environment is activated, then:
```cmd
run_all.bat
```

#### Manual

```bash
python zpt_manager.py        # Manager Bot
python zpt_worker.py         # Worker Bot
python telegram_dashboard.py # Telegram Dashboard Bot
streamlit run dashboard.py   # Streamlit UI
```

### 6. (Optional) Docker Compose

```bash
docker-compose up -d
```

Services:
- `worker`: Worker Bot
- `manager`: Manager Bot
- `telegram_dashboard`: Telegram Dashboard Bot
<!-- Streamlit UI not containerized by default -->

### 7. Testing

```bash
python test_env.py        # Verify required env vars
python test_imports.py    # Quick smoke test of core functions
```

---

## Environment Variables Reference

| Variable             | Description                             |
| -------------------- | --------------------------------------- |
| `OPENAI_API_KEY`     | OpenAI API key (optional)               |
| `METALS_API_KEY`     | Metals-API key for XAUUSD               |
| `BINANCE_API_KEY`    | Binance API key for crypto feeds        |
| `BINANCE_API_SECRET` | Binance API secret                      |
| `BYBIT_API_KEY`      | Bybit API key for crypto fallback       |
| `BYBIT_API_SECRET`   | Bybit API secret                        |
| `MANAGER_BOT_TOKEN`  | Telegram Manager Bot token              |
| `TELEGRAM_BOT_TOKEN` | Telegram Worker Bot token               |
| `ADMIN_ID`           | Telegram user ID for admin actions      |
| `CHANNEL_ID`         | Telegram channel/group ID               |

---

## Codex CLI (optional)

Inline AI suggestions and explanations:
```bash
codex explain zpt_analysis.py
codex explain zpt_worker.py
codex --auto-edit
codex --full-auto
```

---

© ChatZiPT v4 by Tiffany