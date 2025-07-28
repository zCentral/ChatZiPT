@echo off
REM -------------------------------------------------------------------
REM Run all ChatZiPT dashboard components in separate Command Prompt windows
REM -------------------------------------------------------------------

REM Activate Python virtual environment
call "%~dp0.venv\Scripts\activate.bat"

start "Manager Bot" cmd /k "python zpt_manager.py"
start "Worker Bot"  cmd /k "python zpt_worker.py"
start "Telegram Dash Bot" cmd /k "python telegram_dashboard.py"
start "Streamlit UI"   cmd /k "streamlit run dashboard.py"
echo All ChatZiPT services have been started.