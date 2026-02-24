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

# ===== YOUR CONFIGURATION =====
BOT_TOKEN = "8232745888:AAHRWZT7-3vJG-2C0TbbEx0q1VafS_AaVo8"
CHANNEL_ID = -1003756088749
BOT_USERNAME = "Btcdkminingbot"
YOUR_USER_ID = 6423899796
BOT_LINK = f"https://t.me/{BOT_USERNAME}/app?startapp"
# =============================

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
⏱️ {datetime.now().strftime('%-m/%-d %I:%M %p')}""",

        lambda: f"""✅ **Mining Confirmed**

👤 Miner ID: {generate_user_id()}
⛏️ Mined: {random.uniform(10, 200):.2f} USDT
📊 Hash Rate: {random.randint(100, 1000)} MH/s

📝 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%-m/%-d %I:%M %p')}""",

        lambda: f"""💎 **New Mining Reward**

🆔 User: {generate_user_id()}
⛏️ Amount: {random.uniform(1, 100):.3f} USDT
⚡️ Mining Speed: {random.randint(50, 500)} H/s

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%-m/%-d %I:%M %p')}""",

        lambda: f"""🎉 **Daily Mining Reward**

👤 User: {generate_user_id()}
⛏️ Rewards: {random.uniform(5, 75):.4f} USDT
📈 Hash Power: {random.randint(200, 800)} MH/s

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%-m/%-d %I:%M %p')}""",

        lambda: f"""⚡️ **Mining Reward Credited**

🆔 User: {generate_user_id()}
⛏️ Amount: {random.uniform(15, 150):.3f} USDT
💎 Pool: BtcDk Mining Pool

📝 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%-m/%-d %I:%M %p')}"""
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
⏱️ {datetime.now().strftime('%-m/%-d %I:%M %p')}""",

        lambda: f"""✅ **Withdrawal Completed**

🆔 Miner: {generate_user_id()}
💎 Amount: {random.uniform(10, 200):.2f} USDT
⛏️ Status: Confirmed

📝 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%-m/%-d %I:%M %p')}""",

        lambda: f"""💸 **Withdrawal Confirmed**

👤 User ID: {generate_user_id()}
💰 Amount: {random.uniform(25, 300):.3f} USDT
⛏️ Method: USDT (TRC-20)

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%-m/%-d %I:%M %p')}"""
    ]
    
    contract_notifications = [
        lambda: f"""📋 **Mining Contract Purchased**

👤 User: {generate_user_id()}
⛏️ Hash Power: {random.randint(100, 1000)} MH/s
💰 Price: {random.uniform(50, 500):.2f} USDT
📅 Duration: {random.choice(['7 Days', '30 Days', '90 Days', '180 Days'])}

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%-m/%-d %I:%M %p')}""",

        lambda: f"""🎯 **New Mining Contract**

👤 User: {generate_user_id()}
⛏️ Hash Rate: {random.randint(500, 2000)} GH/s
💎 Contract: {random.choice(['Basic', 'Pro', 'Enterprise'])} Mining
💰 Invested: {random.uniform(100, 1000):.2f} USDT

📝 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%-m/%-d %I:%M %p')}"""
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
⏱️ {datetime.now().strftime('%-m/%-d %I:%M %p')}""",

        lambda: f"""✅ **Deposit Confirmed**

👤 User: {generate_user_id()}
💰 Amount: {random.uniform(100, 1000):.2f} USDT
⛏️ Purpose: Hash Power Purchase

📝 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%-m/%-d %I:%M %p')}"""
    ]
    
    all_notifications = mining_notifications + withdrawal_notifications + contract_notifications + deposit_notifications
    notification_func = random.choice(all_notifications)
    message = notification_func()
    
    keyboard = [
        [InlineKeyboardButton("⚡️ Start Mining", url=BOT_LINK)],
        [InlineKeyboardButton("📊 Dashboard", url=f"{BOT_LINK}&start=dashboard")],
        [InlineKeyboardButton("💎 Buy Hash Power", url=f"{BOT_LINK}&start=buy")]
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

async def auto_post_withdrawal(context: ContextTypes.DEFAULT_TYPE):
    message = f"""💸 **Withdrawal Processed**

👤 User: {generate_user_id()}
💰 Amount: {random.uniform(10, 200):.2f} USDT
⛏️ Mining Rewards

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%-m/%-d %I:%M %p')}"""
    
    keyboard = [[InlineKeyboardButton("⚡️ Start Mining", url=BOT_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            parse_mode='Markdown',
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
        logger.info("✅ Withdrawal notification auto-posted")
    except Exception as e:
        logger.error(f"❌ Auto-post failed: {e}")

async def auto_post_contract(context: ContextTypes.DEFAULT_TYPE):
    message = f"""📋 **Mining Contract Purchased**

👤 User: {generate_user_id()}
⛏️ Hash Power: {random.randint(100, 1000)} MH/s
💰 Price: {random.uniform(50, 500):.2f} USDT
📅 Duration: {random.choice(['7 Days', '30 Days', '90 Days'])}

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%-m/%-d %I:%M %p')}"""
    
    keyboard = [[InlineKeyboardButton("⚡️ Start Mining", url=BOT_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            parse_mode='Markdown',
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
        logger.info("✅ Contract notification auto-posted")
    except Exception as e:
        logger.error(f"❌ Auto-post failed: {e}")

async def auto_post_deposit(context: ContextTypes.DEFAULT_TYPE):
    message = f"""💰 **New Deposit Confirmed**

🆔 User: {generate_user_id()}
💵 Amount: {random.uniform(50, 500):.2f} USDT
⛏️ Plan: Mining Investment

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%-m/%-d %I:%M %p')}"""
    
    keyboard = [[InlineKeyboardButton("⚡️ Start Mining", url=BOT_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            parse_mode='Markdown',
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
        logger.info("✅ Deposit notification auto-posted")
    except Exception as e:
        logger.error(f"❌ Auto-post failed: {e}")

def main():
    """Start the bot with auto-posting"""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("send", send_now_command))
    application.add_handler(CommandHandler("status", status_command))

    job_queue = application.job_queue
    
    if job_queue:
        job_queue.run_repeating(auto_post_mining, interval=1800, first=10)
        job_queue.run_repeating(auto_post_withdrawal, interval=2700, first=30)
        job_queue.run_repeating(auto_post_contract, interval=3600, first=60)
        job_queue.run_repeating(auto_post_deposit, interval=5400, first=120)
        logger.info("✅ Auto-posting jobs scheduled")
    else:
        logger.warning("⚠️ Job queue not available")

    print("🤖 BtcDk Mining Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
