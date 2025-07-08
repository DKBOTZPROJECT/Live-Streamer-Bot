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


# /plan Cmd
@DKBOTZ.on_message(filters.command("plan"))
async def dkbotz_plan_command(bot, message):
    await message.reply_text(
        PLAN_DETAILS_TEXT,
        reply_markup=dkbotz_plan_buttons(),
        disable_web_page_preview=True
    )

# /buy Cmd
@DKBOTZ.on_message(filters.command("buy"))
async def dkbotz_buy_command(bot, message):
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=QR_IMAGE_URL,
        caption=PAYMENT_INFO_TEXT,
        reply_markup=dkbotz_payment_buttons()
    )



# Callback
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
    elif data == "plans":
        await query.message.edit_text(
            PLAN_DETAILS_TEXT,
            reply_markup=dkbotz_plan_buttons(),
            disable_web_page_preview=True
        )
    elif data == "buy_now":
        await query.message.delete()

        await bot.send_photo(
            chat_id=query.message.chat.id,
            photo=QR_IMAGE_URL,
            caption=PAYMENT_INFO_TEXT,
            reply_markup=dkbotz_payment_buttons()
        )
