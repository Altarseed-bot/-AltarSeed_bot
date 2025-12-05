import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load bot token from Railway environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise SystemExit("❌ BOT_TOKEN environment variable is missing!")

# API endpoints
GECKO_POOL = "https://api.geckoterminal.com/api/v2/networks/base/pools/0xae6dcae099c4c3e714cb7a2a42e71d0be3f24520"
WHITEPAPER_URL = "https://seedaltar.com/whitepaper.pdf"

# ============================
#   COMMANDS
# ============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🌱 *WELCOME TO ALTAR SEED BOT* 🌱\n\n"
        "You are now connected to the spiritual heart of the ALTAR SEED project — "
        "where intention becomes manifestation.\n\n"
        "Use the commands below:\n\n"
        "• /stat — Live token stats\n"
        "• /chart — Live chart\n"
        "• /links — All official links\n"
        "• /roadmap — Project roadmap\n"
        "• /whitepaper — Whitepaper\n"
        "• /community — Join the community\n"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get(GECKO_POOL, timeout=10)
        r.raise_for_status()
        j = r.json()

        data = j.get("data", {}).get("attributes", {})
        price = data.get("base_token_price_usd", "N/A")
        volume = data.get("volume_usd", {}).get("h24", "N/A")
        liquidity = data.get("reserve_in_usd", "N/A")

    except Exception as e:
        logger.exception("Error fetching stats: %s", e)
        price = volume = liquidity = "Unavailable"

    msg = (
        "📊 *ALTAR SEED — Live Stats*\n\n"
        f"💰 Price: ${price}\n"
        f"📈 24h Volume: ${volume}\n"
        f"🌊 Liquidity: ${liquidity}\n\n"
        "Powered by GeckoTerminal."
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        "https://www.geckoterminal.com/base/pools/0xae6dcae099c4c3e714cb7a2a42e71d0be3f24520"
    )


async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🔗 *ALTAR SEED — Official Links*\n\n"
        "🌐 Website: https://seedaltar.com\n"
        "📊 GeckoTerminal: https://www.geckoterminal.com/base/pools/0xae6dcae099c4c3e714cb7a2a42e71d0be3f24520\n"
        "📜 Contract: 0xab3f042069a7d819dc233025224c3c3ad7c88302\n\n"
        "🕊 Twitter: https://twitter.com/seedaltar\n"
        "💬 Telegram: https://t.me/seedaltar"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📜 *ALTAR SEED ROADMAP*\n\n"
        "🔥 Phase 1 — Creation\n"
        "• Token birth\n"
        "• Contract verification\n"
        "• Whitepaper release\n"
        "• Socials launch\n\n"
        "🌱 Phase 2 — Growth\n"
        "• Community expansion\n"
        "• Bot + Dashboard\n"
        "• Liquidity growth\n\n"
        "🌕 Phase 3 — Ascension\n"
        "• Staking\n"
        "• Marketplace\n"
        "• Cross-chain expansion\n"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def whitepaper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_document(WHITEPAPER_URL)


async def community(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🤝 *Join the ALTAR SEED Community*\n\n"
        "Telegram: https://t.me/seedaltar\n"
        "Discord: https://discord.gg/seedaltar"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


# ============================
#   MAIN APP
# ============================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stat", stat))
    app.add_handler(CommandHandler("chart", chart))
    app.add_handler(CommandHandler("links", links))
    app.add_handler(CommandHandler("roadmap", roadmap))
    app.add_handler(CommandHandler("whitepaper", whitepaper))
    app.add_handler(CommandHandler("community", community))

    # Start polling
    app.run_polling()


if __name__ == "__main__":
    main()
