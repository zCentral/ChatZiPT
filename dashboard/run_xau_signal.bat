https://github.com/zCentral/ChatZiPT/blob/main/dashboard/dashboard.py@echo off
REM ------------------------------------------------------------------
REM Run the XAUUSD bullish engulfing entry script
REM ------------------------------------------------------------------
REM Load METALS_API_KEY from .env (adjacent to this script) if not set
for /f "usebackq tokens=2 delims==" %%K in (`findstr /b "METALS_API_KEY=" "%~dp0\.env"`) do (
    if not defined METALS_API_KEY set "METALS_API_KEY=%%K"
)
pushd "%~dp0"
python xau_signal.py
popd