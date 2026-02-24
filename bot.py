import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import random
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== CONFIGURATION FROM ENVIRONMENT VARIABLES =====
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = int(os.environ.get('CHANNEL_ID', -1003756088749))
YOUR_USER_ID = int(os.environ.get('YOUR_USER_ID', 6423899796))
BOT_USERNAME = "Btcdkminingbot"
BOT_LINK = f"https://t.me/{BOT_USERNAME}/app?startapp"
# ====================================================

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables!")

def generate_tx_hash():
    return '0x' + ''.join(random.choices('abcdef0123456789', k=40))

def generate_user_id():
    return str(random.randint(1000000000, 9999999999))

async def send_mining_notification(context: ContextTypes.DEFAULT_TYPE, chat_id=None):
    """Send a mining notification to channel"""
    
    mining_notifications = [
        lambda: f"""⛏️ **New Mining Reward**

🆔 User: {generate_user_id()}
💰 Amount: {random.uniform(0.5, 50):.4f} USDT
💎 Plan: Cloud Mining (24H)

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}""",

        lambda: f"""✅ **Mining Confirmed**

👤 Miner ID: {generate_user_id()}
⛏️ Mined: {random.uniform(10, 200):.2f} USDT
📊 Hash Rate: {random.randint(100, 1000)} MH/s

📝 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}""",

        lambda: f"""💎 **New Mining Reward**

🆔 User: {generate_user_id()}
⛏️ Amount: {random.uniform(1, 100):.3f} USDT
⚡️ Mining Speed: {random.randint(50, 500)} H/s

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}"""
    ]
    
    withdrawal_notifications = [
        lambda: f"""💸 **Withdrawal Processed**

👤 User: {generate_user_id()}
💰 Amount: {random.uniform(5, 150):.4f} USDT
⛏️ Source: Mining Rewards

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}""",

        lambda: f"""✅ **Withdrawal Completed**

🆔 Miner: {generate_user_id()}
💎 Amount: {random.uniform(10, 200):.2f} USDT
⛏️ Status: Confirmed

📝 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}"""
    ]
    
    contract_notifications = [
        lambda: f"""📋 **Mining Contract Purchased**

👤 User: {generate_user_id()}
⛏️ Hash Power: {random.randint(100, 1000)} MH/s
💰 Price: {random.uniform(50, 500):.2f} USDT
📅 Duration: {random.choice(['7 Days', '30 Days', '90 Days'])}

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}"""
    ]
    
    deposit_notifications = [
        lambda: f"""💰 **New Deposit Confirmed**

🆔 User: {generate_user_id()}
💵 Amount: {random.uniform(50, 500):.2f} USDT
⛏️ Plan: Mining Investment

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}"""
    ]
    
    all_notifications = mining_notifications + withdrawal_notifications + contract_notifications + deposit_notifications
    notification_func = random.choice(all_notifications)
    message = notification_func()
    
    keyboard = [
        [InlineKeyboardButton("⚡️ Start Mining", url=BOT_LINK)],
        [InlineKeyboardButton("📊 Dashboard", url=f"{BOT_LINK}?start=dashboard")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    target_chat = chat_id if chat_id else CHANNEL_ID
    try:
        await context.bot.send_message(
            chat_id=target_chat,
            text=message,
            parse_mode='Markdown',
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
        logger.info(f"✅ Notification sent to channel {target_chat}")
    except Exception as e:
        logger.error(f"❌ Failed to send message: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_msg = f"""👋 Welcome to BtcDk Mining Bot, {user.first_name}!

⛏️ Start cloud mining and earn USDT daily.

🔗 **Join our mining pool:** {BOT_LINK}

**Available Commands:**
/send - Send notification to channel (Owner only)
/status - Check bot status
/help - Show help

⚡️ Powered by BtcDk Mining"""
    
    await update.message.reply_text(welcome_msg, disable_web_page_preview=True)

async def send_now_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == YOUR_USER_ID:
        await send_mining_notification(context, CHANNEL_ID)
        await update.message.reply_text("✅ Notification sent to channel!")
    else:
        await update.message.reply_text("❌ Unauthorized. Only the bot owner can use this command.")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = f"""🤖 **BtcDk Mining Bot Status**

✅ Bot: Online
⛏️ Channel ID: `{CHANNEL_ID}`
🔗 Mining Bot: @{BOT_USERNAME}
📊 Auto-posting: Active
💵 Payment: USDT Only

⚡️ Powered by BtcDk Mining"""
    
    await update.message.reply_text(status_msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = f"""🤖 **BtcDk Mining Bot Commands:**

/send - Manually trigger a notification (Owner only)
/status - Check bot status and settings
/help - Show this help message

**Automatic Features:**
• Mining reward notifications (every 30 min)
• Withdrawal confirmations (every 45 min)
• Contract purchases (every hour)
• Deposit confirmations (random intervals)

**Payment Method:** 💵 USDT Only

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown', disable_web_page_preview=True)

async def auto_post_mining(context: ContextTypes.DEFAULT_TYPE):
    await send_mining_notification(context, CHANNEL_ID)

def main():
    """Start the bot with auto-posting"""
    print("🤖 BtcDk Mining Bot is starting...")
    print(f"📱 Bot: @{BOT_USERNAME}")
    print(f"📢 Channel ID: {CHANNEL_ID}")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("send", send_now_command))
    application.add_handler(CommandHandler("status", status_command))

    # Set up auto-posting
    job_queue = application.job_queue
    if job_queue:
        job_queue.run_repeating(auto_post_mining, interval=1800, first=10)
        print("✅ Auto-posting: Active (every 30 minutes)")
    
    print("⚡️ Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
