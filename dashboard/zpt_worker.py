import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from utils import get_env, log, generate_referral_code, pro_features_unlocked, get_aura_points
from zpt_analysis import analyze
import telegram.ext._updater as _updater_mod
class _PatchedUpdater(_updater_mod.Updater):
    pass
_updater_mod.Updater = _PatchedUpdater
import telegram.ext._applicationbuilder as _appb_mod
_appb_mod.Updater = _PatchedUpdater
from telegram.constants import ParseMode
from zpt_pricefeed import price_health
import openai
import re

try:
    openai.api_key = get_env("OPENAI_API_KEY")
except Exception as e:
    log(f"OpenAI key setup error: {e}", level="ERROR")

TELEGRAM_BOT_TOKEN = get_env("TELEGRAM_BOT_TOKEN")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I am the Worker Bot.\n"
        "Send asset names (e.g. btc, eth, gold) for signals, or /dashboard for system overview."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Welcome message\n"
        "/help - This help text\n"
        "/dashboard - Show system health and AI signals\n"
        "<any text> - Natural analysis or lot size queries"
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
        user_id = update.effective_user.id
        text = update.message.text.lower()
        asset = None
        for coin in ["btc", "eth", "gold", "xauusd"]:
            if coin in text:
                asset = {"btc": "BTC", "eth": "ETH", "gold": "XAUUSD", "xauusd": "XAUUSD"}[coin]
                break
        if asset:
            user_data = {"aura_points": get_aura_points({"id": user_id}), "pro_unlock_code_valid": True}
            result = analyze(asset, user_data)
            msg = (
                f"📈 {asset} Signal\n"
                f"Price: {result['price']}\n"
                f"Action: {result['action']}\n"
                f"Confidence: {int(result['confidence']*100)}%\n"
                f"SL: {result['SLTP']['SL']}, TP: {result['SLTP']['TP']}\n"
                f"Serial: {result['SN']}\n"
                f"AI Reasoning: {result['explanation']}"
            )
            await update.message.reply_text(msg)
            return
        if "lot size" in text or "calculate" in text:
            match = re.search(r"([£$€]?)(\d+(\.\d+)?)", text)
            balance = float(match.group(2)) if match else 30
            risk_pct = 0.02
            sl_pips = 200
            account_currency = match.group(1) if match else "£"
            risk_amount = balance * risk_pct
            lot_size = risk_amount / (sl_pips * 10)
            await update.message.reply_text(
                f"For a {account_currency}{balance} balance on gold/XAUUSD:\n"
                f"- Max risk per trade: {account_currency}{risk_amount:.2f}\n"
                f"- Suggested lot size: {lot_size:.3f}\n"
                f"Adjust lot size for tighter SL/lower risk."
            )
            return
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": update.message.text}],
            max_tokens=200
        )
        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)
    except Exception as e:
        log(f"Worker natural message error: {e}", level="ERROR")
        await update.message.reply_text("Sorry, there was an error processing your request. Please try again or check logs.")

async def _on_startup(app):
    await app.bot.delete_webhook(drop_pending_updates=True)

def main():
    try:
        app = (
            ApplicationBuilder()
            .token(TELEGRAM_BOT_TOKEN)
            .post_init(_on_startup)
            .build()
        )
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("dashboard", dashboard_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, natural_message))
        log("Worker bot running (natural language)...")
        app.run_polling()
    except Exception as e:
        log(f"Worker bot main error: {e}", level="ERROR")

if __name__ == "__main__":
    main()