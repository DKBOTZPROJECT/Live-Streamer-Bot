from pyrogram import Client as DKBOTZ, filters
from pyrogram.types import *
from Config import *
from text import *



# /start cmd
@DKBOTZ.on_message(filters.command("start"))
async def dkbotz_handle_start(bot, message):
    await message.reply_text(
        START_MESSAGE,
        reply_markup=start_buttons(),
        disable_web_page_preview=True
    )

# /help cmd
@DKBOTZ.on_message(filters.command("help"))
async def dkbotz_help_command(bot, message):
    await message.reply_text(
        HELP_MESSAGE,
        reply_markup=dkbotz_help_buttons(),
        disable_web_page_preview=True
    )









@DKBOTZ.on_callback_query()
async def dkbotz_handle_callbacks(bot, query):
    data = query.data
    if data == "home":
        await query.message.edit_text(
            START_MESSAGE,
            reply_markup=start_buttons(),
            disable_web_page_preview=True
        )

    elif data == "help":
        await query.message.edit_text(
            HELP_MESSAGE,
            reply_markup=dkbotz_help_buttons(),
            disable_web_page_preview=True
        )

