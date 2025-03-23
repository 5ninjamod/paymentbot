import os
import logging
import asyncio
from telethon import TelegramClient, events
from datetime import datetime

# API credentials (Directly set here instead of .env)
API_ID = 22627280  # Replace with your actual API ID
API_HASH = "b2e5eb5e3dd886f5b8be6a749a26f619"  # Replace with your actual API Hash
OWNER_ID = 1240179115  # Replace with your Telegram User ID

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate API credentials
if not API_ID or not API_HASH:
    logger.error("API_ID or API_HASH is missing. Check your configuration.")
    exit(1)

# Initialize Telegram client
client = TelegramClient('session_name', API_ID, API_HASH)

# Configuration
channel_link = "https://t.me/+lgb92RXeI2E4ZjM1"
price_list_link = "https://t.me/c/2147999578/8855"  # Replace with your actual price list link
qr_code_path = 'payment.jpg'
gif_path = '0.gif'
cooldown_period = 600  # 10 minutes
last_qr_request = {}

help_message = """
🤖 **Available Commands:**

- **`qr`** → Get the QR code for payment
- **`free`** → **🖕🏻 FREE ME TO LODA MILEGA! 🖕🏻**
- **`channel`**, **`channel link`**, **`link`** → Get the channel link
- **`price`** → Get the price list link
- **`help`** → Show this help message
- **`/id`** → Get your own Telegram ID
- **`/id @username`** (Owner Only) → Get user ID of a specific user
"""

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        user_id = event.sender_id
        message_text = event.raw_text.lower()
        
        # Handle QR requests with cooldown
        if 'qr' in message_text:
            now = datetime.now()
            if user_id in last_qr_request and (now - last_qr_request[user_id]).total_seconds() < cooldown_period:
                await event.reply("🖕🏻 **BSDK RUK JA 10 Min USKE BAAD MILEGA QR.** 🖕🏻")
                return
            await client.send_file(event.chat_id, qr_code_path, caption=f"**Here is my QR code for payment.**\n{channel_link}", force_document=False, allow_cache=True)
            last_qr_request[user_id] = now
        
        # Free message response
        elif 'free' in message_text:
            await event.reply("🖕🏻 **FREE ME TO LODA MILEGA!** 🖕🏻")
        
        # Channel link response
        elif any(word in message_text for word in ['channel', 'channel link', 'link']):
            await event.reply(f"**My channel link:** {channel_link}")
        
        # Price list response
        elif 'price' in message_text:
            await event.reply(f"🛒 **Here is our price list:** {price_list_link}")
        
        # Help command
        elif 'help' in message_text:
            await event.reply(help_message)
        
        # Send GIF to new users
        elif message_text in ['hi', 'hello', 'hlw', 'hii', 'hey']:
            await client.send_file(event.chat_id, gif_path, caption="**Welcome!**", force_document=False, allow_cache=True)
        
        # ID command
        elif message_text.startswith('/id'):
            parts = message_text.split()
            if len(parts) == 1:
                await event.reply(f"**Your Telegram ID:** `{user_id}`")
            elif len(parts) > 1 and user_id == OWNER_ID:
                try:
                    username = parts[1]
                    entity = await client.get_entity(username)
                    await event.reply(f"**User ID of {username}:** `{entity.id}`")
                except Exception as e:
                    await event.reply("❌ **User not found!**")
                    logger.error(f"Error fetching user ID: {e}")
            elif user_id != OWNER_ID:
                await event.reply("❌ **You are not authorized to check other users' IDs!**")

    except Exception as e:
        logger.error(f"Error handling message: {e}")

# Notify users when they join the channel
@client.on(events.ChatAction)
async def user_joined(event):
    if event.user_joined or event.user_added:
        await event.reply("**THANK YOU FOR JOINING OUR CHANNEL!**")

# Start the client
client.start()
logger.info("Client is running...")
client.run_until_disconnected()
