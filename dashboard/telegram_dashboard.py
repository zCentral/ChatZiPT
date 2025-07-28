from utils import get_env, log

# Monkey‑patch PTB v20.8 Updater to allow dynamic polling cleanup attribute
import telegram.ext._updater as _updater_mod
class _PatchedUpdater(_updater_mod.Updater):
    pass
_updater_mod.Updater = _PatchedUpdater
import telegram.ext._applicationbuilder as _appb_mod
_appb_mod.Updater = _PatchedUpdater

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from zpt_pricefeed import price_health
from zpt_analysis import analyze

import logging
logger = logging.getLogger(__name__)

# Suppress telegram-bot HTTP request & polling info logs for readability
logging.getLogger("telegram").setLevel(logging.WARNING)
logging.getLogger("telegram.ext").setLevel(logging.WARNING)
logging.getLogger("telegram.request").setLevel(logging.WARNING)

TELEGRAM_BOT_TOKEN = get_env("TELEGRAM_BOT_TOKEN")

async def dashboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /dashboard: sends system health and AI signals via Telegram."""
    logger.info("dashboard_command triggered by user_id=%s", update.effective_user.id)
    # System health metrics
    health = price_health()
    health_lines = [f"{k}: {v}" for k, v in health.items()]
    await update.message.reply_text(
        "*System Health:*\n" + "\n".join(health_lines),
        parse_mode=ParseMode.MARKDOWN
    )

    # AI trading signals for core assets
    assets = ["BTC", "ETH", "XAUUSD"]
    for asset in assets:
        res = analyze(asset)
        await update.message.reply_text(
            f"*{asset}* signal: {res['action']}, Confidence: {int(res['confidence']*100)}%",
            parse_mode=ParseMode.MARKDOWN
        )

async def _on_startup(app):
    """Delete any existing webhook and drop pending updates to avoid getUpdates conflicts."""
    logger.info("Running startup: delete webhook and drop pending updates")
    await app.bot.delete_webhook(drop_pending_updates=True)

def main():
    # Build the application, deleting any existing webhook on startup to avoid getUpdates conflicts
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .post_init(_on_startup)
        .build()
    )
    app.add_handler(CommandHandler('dashboard', dashboard_command))
    print("Telegram dashboard bot running. Send /dashboard to receive current metrics.")
    app.run_polling()

if __name__ == '__main__':
    main()