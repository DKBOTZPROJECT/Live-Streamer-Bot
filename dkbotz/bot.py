from pyrogram import Client as DKBOTZ, filters
from pyrogram.types import *
from Config import *
from text import *




@DKBOTZ.on_message(filters.command("start"))
async def handle_start(bot, message):
    await message.reply_text(
        START_MESSAGE,
        reply_markup=start_buttons(),
        disable_web_page_preview=True
    )
