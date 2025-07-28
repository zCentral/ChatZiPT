import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import telegram.ext._updater as _updater_mod
class _PatchedUpdater(_updater_mod.Updater):
    pass
_updater_mod.Updater = _PatchedUpdater
import telegram.ext._applicationbuilder as _appb_mod
_appb_mod.Updater = _PatchedUpdater
from telegram.constants import ParseMode
from zpt_pricefeed import price_health
from utils import get_env, log, generate_referral_code, get_aura_points
from zpt_analysis import analyze, meme_shitcoin_analysis
import openai

try:
    openai.api_key = get_env("OPENAI_API_KEY")
except Exception as e:
    log(f"OpenAI key setup error: {e}", level="ERROR")

MANAGER_BOT_TOKEN = get_env("MANAGER_BOT_TOKEN")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I am the Manager Bot.\n"
        "Send any text to get AI-powered answers, or use /dashboard to view system health and signals."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Welcome message\n"
        "/help - This help text\n"
        "/dashboard - Show system health and AI signals\n"
        "<any text> - Ask me anything!"
    )

async def dashboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    health = price_health()
    health_lines = [f"{k}: {v}" for k, v in health.items()]
    await update.message.reply_text(
        "*System Health:*\n" + "\n".join(health_lines),
        parse_mode=ParseMode.MARKDOWN,
    )
    assets = ["BTC", "ETH", "XAUUSD"]
    for asset in assets:
        res = analyze(asset)
        await update.message.reply_text(
            f"*{asset}* signal: {res['action']}, Confidence: {int(res['confidence']*100)}%",
            parse_mode=ParseMode.MARKDOWN,
        )

async def natural_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.lower()
        if "shitcoin" in text or "meme coin" in text:
            signals = meme_shitcoin_analysis()
            if signals:
                reply = "\n".join([f"{s['symbol']}: score {s['score']:.2f}" for s in signals])
                await update.message.reply_text("Shitcoin signals (90%+):\n" + reply)
            else:
                await update.message.reply_text("No high-potential shitcoin signals now.")
            return
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": update.message.text}],
            max_tokens=200
        )
        await update.message.reply_text(response.choices[0].message.content.strip())
    except Exception as e:
        log(f"Manager natural message error: {e}", level="ERROR")
        await update.message.reply_text("Error processing request. Check logs or try again.")

async def _on_startup(app):
    await app.bot.delete_webhook(drop_pending_updates=True)

def main():
    try:
        app = (
            ApplicationBuilder()
            .token(MANAGER_BOT_TOKEN)
            .post_init(_on_startup)
            .build()
        )
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("dashboard", dashboard_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, natural_message))
        log("Manager bot running (natural language)...")
        app.run_polling()
    except Exception as e:
        log(f"Manager bot main error: {e}", level="ERROR")

if __name__ == "__main__":
    main()