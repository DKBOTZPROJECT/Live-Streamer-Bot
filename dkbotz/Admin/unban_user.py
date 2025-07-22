import logging
import traceback
from Config import *
from helpers import *

log = logging.getLogger(__name__)


@DKBOTZ.on_message(filters.private & filters.command("unban_user") & filters.user(AUTH_USERS))
async def dkbotz_unban_admin(c, m):
    if len(m.command) == 1:
        await m.reply_text(
            "Use this command to unban any user.\n\nUsage:\n\n`/unban_user user_id`\n\n"
            "Eg: `/unban_user 1234567`\n This will unban user with id `1234567`.",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user {user_id}"

        try:
            await c.send_message(
                user_id, "Your ban is lifted.\n\nNow you can use the bot."
            )
            unban_log_text += "\n\nUser notified successfully ✅"
        except Exception as e:
            log.debug(e, exc_info=True)
            unban_log_text += (
                f"\n\nUser notification failed !!! \n\n`{traceback.format_exc()}`"
            )
        db.remove_ban(user_id)
        log.debug(unban_log_text)
        await m.reply_text(unban_log_text, quote=True)
    except Exception as e:
        log.error(e, exc_info=True)
        await m.reply_text(
            f"Error occoured! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True,
        )
