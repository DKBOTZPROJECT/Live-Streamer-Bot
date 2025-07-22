from Config import *
from helpers import *


@DKBOTZ.on_message(filters.private & filters.command("status") & filters.user(AUTH_USERS))
async def dkbotz_status_admin(c, m):
    total_users = db.total_users_count()
    text = f"Total users till date : {total_users}"
    await m.reply_text(text=text, quote=True)
