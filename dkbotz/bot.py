from pyrogram import Client as DKBOTZ, filters
from pyrogram.types import *
from Config import *
from text import *

@DKBOTZ.on_message(filters.command("start"))
async def start(client, message):
    keyboard = InlineKeyboardMarkup(
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
    await message.reply_text(
        START_MESSAGE,
        reply_markup=keyboard,
    )
