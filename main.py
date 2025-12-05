import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Bot token from Railway environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise SystemExit("❌ BOT_TOKEN not set in environment variables.")

# Constants
GECKO_POOL = "https://api.geckoterminal.com/api/v2/networks/base/pools/0xae6dcae099c4c3e714cb7a2a42e71d0be3f24520"
WHITEPAPER_URL = "https://seedaltar.com/whitepaper.pdf"

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """🌱 *WELCOME TO ALTAR SEED BOT* 🌱

You are now connected to the spiritual heart of the ALTAR SEED project.

Use the commands below to explore:

• /stat — Live token stats
• /chart — Live chart
• /links — All official links
• /roadmap — Project roadmap
• /whitepaper — Whitepaper
• /community — Join community
"""
    await update.message.reply_text(msg, parse_mode="Markdown")

async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get(GECKO_POOL, timeout=10)
        r.raise_for_status()
        data = r.json().get("data", {}).get("attributes", {})
        price = data.get("base_token_price_usd", "N/A")
        volume = data.get("volume_usd", {}).get("h24", "N/A")
        liquidity = data.get("reserve_in_usd", "N/A")
    except Exception:
        price = volume = liquidity = "Unavailable"

    msg = f"""
📊 *ALTAR SEED — Live Stats*

💰 Price: ${price}
📈 24h Volume: ${volume}
🌊 Liquidity: ${liquidity}

Powered by GeckoTerminal.
"""
    await update.message.reply_text(msg, parse_mode="Markdown")

async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo("https://www.geckoterminal.com/base/pools/0xae6dcae099c4c3e714cb7a2a42e71d0be3f24520")

async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
🔗 *ALTAR SEED — Official Links*

🌐 Website: https://seedaltar.com
📊 GeckoTerminal: https://www.geckoterminal.com/base/pools/0xae6dcae099c4c3e714cb7a2a42e71d0be3f24520
📜 Contract: 0xab3f042069a7d819dc233025224c3c3ad7c88302

🕊 Twitter: https://twitter.com/seedaltar
💬 Telegram: https://t.me/seedaltar
"""
    await update.message.reply_text(msg, parse_mode="Markdown")

async def roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
📜 *ALTAR SEED ROADMAP*

🔥 Phase 1 — Creation
• Token birth
• Smart contract verification
• Whitepaper release
• Social media launch

🌱 Phase 2 — Growth
• Community expansion
• Bot + Dashboard
• Liquidity strengthening

🌕 Phase 3 — Ascension
• Staking
• Marketplace
• Cross-chain expansion
"""
    await update.message.reply_text(msg, parse_mode="Markdown")

async def whitepaper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_document(WHITEPAPER_URL)

async def community(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
🤝 *Join the ALTAR SEED Community*

Telegram: https://t.me/seedaltar
Discord: https://discord.gg/seedaltar
"""
    await update.message.reply_text(msg, parse_mode="Markdown")

# Main
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stat", stat))
    app.add_handler(CommandHandler("chart", chart))
    app.add_handler(CommandHandler("links", links))
    app.add_handler(CommandHandler("roadmap", roadmap))
    app.add_handler(CommandHandler("whitepaper", whitepaper))
    app.add_handler(CommandHandler("community", community))

    # Run bot
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
