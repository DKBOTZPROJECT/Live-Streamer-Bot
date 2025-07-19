from pyrogram import Client as DKBOTZ, filters
from pyrogram.types import *
from Config import *
from text import *
from helpers import *
from datetime import datetime
import pytz


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
    elif data.startswith("refresh_"):
        stream_id = data.split("_")[1]

        dkbotz = get_task_status(PREMIUM_USERNAME, PREMIUM_PASSWORD, stream_id, PRODUCT_NAME)
        if not dkbotz["status"]:
            await query.answer("⏳ Wait! Your Task Has Not Started Yet.\nPlease wait 2 minutes.", show_alert=True)
            return
        
        stream_status = dkbotz["task"]['task']
        stream_msg = dkbotz['task']["message"]
        time = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y %I:%M:%S %p")

        await query.answer("🔄 Status Refreshed!")
        await query.message.edit_text(f"✅ <b>Stream Status Refreshed</code>\n\n📡 <b>Status:</b> {stream_status}\n\n📝 <b>Info:</b> {stream_msg}\n\n🕒 <b>Updated at:</b> <code>{time}</code>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_{stream_id}")], [InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{DEVELOPER_USERNAME}")]]))
