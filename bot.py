#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import sys
import random
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Fix for Python 3.13 compatibility
if sys.version_info >= (3, 13):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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
    raise ValueError("❌ No BOT_TOKEN found in environment variables!")

def generate_tx_hash():
    """Generate random transaction hash"""
    return '0x' + ''.join(random.choices('abcdef0123456789', k=40))

def generate_user_id():
    """Generate random user ID"""
    return str(random.randint(1000000000, 9999999999))

async def send_mining_notification(context: ContextTypes.DEFAULT_TYPE, chat_id=None):
    """Send a mining notification to channel"""
    
    # Mining reward notifications
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
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}""",

        lambda: f"""🎉 **Daily Mining Reward**

🆔 User: {generate_user_id()}
⛏️ Rewards: {random.uniform(5, 75):.4f} USDT
📈 Hash Power: {random.randint(200, 800)} MH/s

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}""",

        lambda: f"""⚡️ **Mining Reward Credited**

🆔 User: {generate_user_id()}
⛏️ Amount: {random.uniform(15, 150):.3f} USDT
💎 Pool: BtcDk Mining Pool

📝 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}"""
    ]
    
    # Withdrawal notifications
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
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}""",

        lambda: f"""💸 **Withdrawal Confirmed**

👤 User ID: {generate_user_id()}
💰 Amount: {random.uniform(25, 300):.3f} USDT
⛏️ Method: USDT (TRC-20)

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}"""
    ]
    
    # Contract purchase notifications
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
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}""",

        lambda: f"""🎯 **New Mining Contract**

👤 User: {generate_user_id()}
⛏️ Hash Rate: {random.randint(500, 2000)} GH/s
💎 Contract: {random.choice(['Basic', 'Pro', 'Enterprise'])} Mining
💰 Invested: {random.uniform(100, 1000):.2f} USDT

📝 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}"""
    ]
    
    # Deposit notifications
    deposit_notifications = [
        lambda: f"""💰 **New Deposit Confirmed**

🆔 User: {generate_user_id()}
💵 Amount: {random.uniform(50, 500):.2f} USDT
⛏️ Plan: Mining Investment

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}""",

        lambda: f"""✅ **Deposit Confirmed**

👤 User: {generate_user_id()}
💰 Amount: {random.uniform(100, 1000):.2f} USDT
⛏️ Purpose: Hash Power Purchase

📝 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}"""
    ]
    
    # Combine all notifications
    all_notifications = (mining_notifications + withdrawal_notifications + 
                        contract_notifications + deposit_notifications)
    notification_func = random.choice(all_notifications)
    message = notification_func()
    
    # Create inline keyboard
    keyboard = [
        [InlineKeyboardButton("⚡️ Start Mining", url=BOT_LINK)],
        [InlineKeyboardButton("📊 Dashboard", url=f"{BOT_LINK}?start=dashboard")],
        [InlineKeyboardButton("💎 Buy Hash Power", url=f"{BOT_LINK}?start=buy")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send to channel
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
    """Handle /start command"""
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
    """Handle /send command - manual notification"""
    if update.effective_user.id == YOUR_USER_ID:
        await send_mining_notification(context, CHANNEL_ID)
        await update.message.reply_text("✅ Notification sent to channel!")
    else:
        await update.message.reply_text("❌ Unauthorized. Only the bot owner can use this command.")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    status_msg = f"""🤖 **BtcDk Mining Bot Status**

✅ Bot: Online
⛏️ Channel ID: `{CHANNEL_ID}`
🔗 Mining Bot: @{BOT_USERNAME}
📊 Auto-posting: Active (every 30 min)
💵 Payment: USDT Only

⚡️ Powered by BtcDk Mining"""
    
    await update.message.reply_text(status_msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
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
    """Auto post mining notifications"""
    await send_mining_notification(context, CHANNEL_ID)

async def auto_post_withdrawal(context: ContextTypes.DEFAULT_TYPE):
    """Auto post withdrawal notifications"""
    message = f"""💸 **Withdrawal Processed**

👤 User: {generate_user_id()}
💰 Amount: {random.uniform(10, 200):.2f} USDT
⛏️ Mining Rewards

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}"""
    
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
    """Auto post contract notifications"""
    message = f"""📋 **Mining Contract Purchased**

👤 User: {generate_user_id()}
⛏️ Hash Power: {random.randint(100, 1000)} MH/s
💰 Price: {random.uniform(50, 500):.2f} USDT
📅 Duration: {random.choice(['7 Days', '30 Days', '90 Days'])}

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}"""
    
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
    """Auto post deposit notifications"""
    message = f"""💰 **New Deposit Confirmed**

🆔 User: {generate_user_id()}
💵 Amount: {random.uniform(50, 500):.2f} USDT
⛏️ Plan: Mining Investment

🔗 **TX:**
{generate_tx_hash()}

⚡️ Powered by BtcDk Mining
🔗 {BOT_LINK}
⏱️ {datetime.now().strftime('%m/%d %I:%M %p')}"""
    
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
    """Main function to start the bot"""
    print("=" * 50)
    print("🤖 BtcDk Mining Bot is starting...")
    print(f"📱 Bot: @{BOT_USERNAME}")
    print(f"📢 Channel ID: {CHANNEL_ID}")
    print(f"👑 Owner ID: {YOUR_USER_ID}")
    print("=" * 50)
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("send", send_now_command))
    application.add_handler(CommandHandler("status", status_command))

    # Set up auto-posting jobs
    job_queue = application.job_queue
    if job_queue:
        job_queue.run_repeating(auto_post_mining, interval=1800, first=10)
        job_queue.run_repeating(auto_post_withdrawal, interval=2700, first=30)
        job_queue.run_repeating(auto_post_contract, interval=3600, first=60)
        job_queue.run_repeating(auto_post_deposit, interval=5400, first=120)
        print("✅ Auto-posting: Active")
        print("   ⏱️  Mining: every 30 min")
        print("   ⏱️  Withdrawal: every 45 min")
        print("   ⏱️  Contract: every 60 min")
        print("   ⏱️  Deposit: every 90 min")
    else:
        print("⚠️ Auto-posting: Not available")
    
    print("⚡️ Bot is running... Press Ctrl+C to stop")
    print("=" * 50)
    
    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
