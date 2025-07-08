from pyrogram import Client as DKBOTZ, filters
from pyrogram.types import *
from Config import *

START_MESSAGE = """🎥 <b>Welcome To The YouTube Live Streamer Bot!</b>

✨ I Am Here To Help You Stream <b>24/7 Videos</b> On:
🔴 <b>YouTube
🔵 Facebook
🟣 And Many Other Platforms!</b>

💡 Whether You Are A Creator, Brand, Or Business, I Will Make Your <b>Live Streaming</b> Easy And Non-Stop For You.

ℹ️ <b>Want To Know More?</b> 
👉 Tap The Buttons Below!
"""

def start_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("💰 Plans", callback_data="plans"),
                InlineKeyboardButton("ℹ️ Help", callback_data="help")
            ],
            [
                InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{DEVELOPER_USERNAME}"),
                InlineKeyboardButton("📢 Channel", url=f"https://t.me/{CHANNEL_USERNAME}")
            ]
        ]
    )
