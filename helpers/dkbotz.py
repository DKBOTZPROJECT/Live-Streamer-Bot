import requests
import os
import random
import string
from Config import *
from text import *
from .db import *
from pyrogram.types import *
import datetime


def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def check_video_link(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)

        if response.status_code != 200:
            return False

        content_type = response.headers.get("Content-Type", "")

        if content_type.startswith("video/") and content_type in ALLOWED_MIME_TYPES:
            return True
        else:
            return False

    except requests.RequestException:
        return False

def add_new_user(user_id):
    if not db.is_user_exist(user_id):
        db.add_user(user_id)


async def premium_check(c, m):
    user_id = m.from_user.id

    if PAID_BOT.upper() == "YES":
        try:
            paid_status = db.get_paid_status(user_id)
        except:
            await m.reply_text("⚠️ Please Click On /start First And Try Again.")
            return False

        if paid_status["is_paid"]:
            current_date = datetime.datetime.now()
            paid_duration = paid_status["paid_duration"]
            paid_on = paid_status["paid_on"]
            paid_reason = paid_status["paid_reason"]

            if isinstance(paid_on, str):
                try:
                    paid_on = datetime.datetime.strptime(paid_on, '%Y-%m-%d %H:%M:%S')
                except:
                    await m.reply_text("❌ Issue In Your Plan. Please Contact Admin.")
                    return False

            try:
                duration_days = int(paid_duration)
            except:
                duration_days = 0

            will_expire = paid_on + datetime.timedelta(days=duration_days)

            if will_expire < current_date:
                try:
                    db.remove_paid(user_id)
                except:
                    pass

                try:
                    await m.reply_text(text=f"📅 Your Paid Plan Has Expired On: <b>{will_expire.strftime('%Y-%m-%d %H:%M:%S')}</b>\n\n💳 If You Want To Continue Using This Bot, Please Subscribe Again By Clicking The Button Below 👇", reply_markup=dkbotz_payment_buttons(), disable_web_page_preview=True)
                except:
                    pass
                for admin_id in AUTH_USERS:

                    try:

                        await c.send_message(admin_id, text=f"🔔 <b>Plan Expired Alert</b> 🔔\n\n🆔 User ID: `{user_id}`\n👤 Username: @{m.from_user.username or 'N/A'}\n📆 Plan Duration: {paid_duration} Days\n📥 Subscribed On: {paid_on.strftime('%Y-%m-%d %H:%M:%S')}\n📝 Plan Description: {paid_reason}")
                    except:
                        pass
                        
                return False
            else:
                return True
        else:
            await m.reply_text(text=f"<b>🚫 You Don’t Have Any Active Plan For This Bot.\n\n💡 Click The Button Below To Subscribe And Start Using The Bot. 👇\n\n👉 Click On The 💰 Plans Button Below Or Send /plan To View Available Plans.</b>", reply_markup=dkbotz_payment_buttons(), disable_web_page_preview=True)
            return False
    else:
        return True
