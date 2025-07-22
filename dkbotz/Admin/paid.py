import asyncio
import datetime
import io
import logging
import os
import random
import string
import time
import traceback
import aiofiles
from Config import *
from helpers import *

log = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)



broadcast_ids = {}


async def send_msg(user_id, message):
    try:
        await message.forward(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception:
        return 500, f"{user_id} : {traceback.format_exc()}\n"


@DKBOTZ.on_message(filters.command("paid_broadcast") & filters.private & filters.user(AUTH_USERS) & filters.reply)
async def dkbotz_paidbroadcast_admin(c, m):
    all_users = db.get_all_paid_users()
    total_users = 0
    async for paid_user in all_users:
        total_users += 1

    broadcast_msg = m.reply_to_message
    while True:
        broadcast_id = "".join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    out = await m.reply_text(text=f"Broadcasting.....")
    start_time = time.time()
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = dict(
        total=total_users, current=done, failed=failed, success=success
    )
    async with aiofiles.open("broadcast.txt", "w") as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(user_id=int(user["id"]), message=broadcast_msg)
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            # if sts == 400:
            #    db.delete_user(user['id'])
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(
                    dict(current=done, failed=failed, success=success)
                )
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()
    if failed == 0:
        await m.reply_text(
            text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True,
        )
    else:
        await m.reply_document(
            document="broadcast.txt",
            caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True,
        )
    os.remove("broadcast.txt")


async def check_user_plan(c, m):
    paid_duration = 0
    paid_on = 0
    paid_usr_count = 0
    will_expire_on_date = 0
    will_expire_days = 0
    try:
        user_ids = int(m.from_user.id)
        all_paid_users = db.get_all_paid_users()
        async for paid_user in all_paid_users:
            user_id = paid_user["id"]
            if user_ids == user_id:
                paid_duration = paid_user["paid_status"]["paid_duration"]
                paid_on = paid_user["paid_status"]["paid_on"]
                paid_user["paid_status"]["paid_username"]
                paid_user["paid_status"]["paid_reason"]
                paid_usr_count = 1

                current_date = datetime.datetime.now()
                integer_paid_duration = int(paid_duration)
                will_expire = paid_on + datetime.timedelta(days=integer_paid_duration)

                if will_expire < current_date:
                    db.remove_paid(user_id)
                    paid_usr_count = 0
                    return (
                        paid_usr_count,
                        paid_on,
                        paid_duration,
                        will_expire_days,
                        will_expire_on_date,
                    )
                will_exp_days = will_expire - current_date  # 29 days, 23:59:48.762168
                # formatted
                will_expire_on_date = will_expire.strftime("%Y-%m-%d")  # 2022-08-12
                will_expire_days = will_exp_days

                return (
                    paid_usr_count,
                    paid_on,
                    paid_duration,
                    will_expire_days,
                    will_expire_on_date,
                )
        if paid_usr_count == 0:
            return (
                paid_usr_count,
                paid_on,
                paid_duration,
                will_expire_days,
                will_expire_on_date,
            )
    except Exception as e:
        log.error(e, exc_info=True)
        paid_usr_count = 0
        return (
            paid_usr_count,
            paid_on,
            paid_duration,
            will_expire_days,
            will_expire_on_date,
        )


@DKBOTZ.on_message(filters.private & filters.command("paid") & filters.user(AUTH_USERS))
async def dkbotz_paid_ss_admin(c, m):
    await m.reply_text(
        "➩  /paid_user Add a user in Subscription\n\n➩  /paid_status To know user(s) paid status"
        "\n\n➩  /plan_expired When plan expired\n\n➩  /paid_users List of all paid users",
        quote=True,
    )


@DKBOTZ.on_message(filters.private & filters.command("paid_status") & filters.user(AUTH_USERS))
async def dkbotz_paid_statusss_admin(c, m):
    if len(m.command) == 1:
        await m.reply_text(
            "Use this command to add a user in paid bot.\n\nUsage:\n\n`/paid_user user_id`",
            quote=True,
        )
        return

    try:
        user_ids = int(m.command[1])
        all_paid_users = db.get_all_paid_users()
        text = ""
        paid_usr_count = 0
        async for paid_user in all_paid_users:
            user_id = paid_user["id"]
            if user_ids == user_id:
                paid_usr_count += 1
                paid_duration = paid_user["paid_status"]["paid_duration"]
                paid_on = paid_user["paid_status"]["paid_on"]
                paid_username = paid_user["paid_status"]["paid_username"]
                paid_reason = paid_user["paid_status"]["paid_reason"]
                text += f"✶ **User Id** : `{user_id}`\n\n✶ **User Name** : {paid_username}\n\n➩ **Plan Validity** : `{paid_duration}` Days\n\n➩ **Joined On** : {paid_on} \n\n➩ **Discription** : `{paid_reason}` \n\n"
        if paid_usr_count == 0:
            await m.reply_text(
                "⚠️ Paid User not found in this id, or Plan Expired ",
                quote=True,
            )
            return
        reply_text = f"{text}"
        if len(reply_text) > 4096:
            paid_usrs = io.BytesIO()
            paid_usrs.name = "paid-users.txt"
            paid_usrs.write(reply_text.encode())
            await m.reply_document(paid_usrs, True)
            return
        await m.reply_text(reply_text, True)
    except Exception as e:
        log.error(e, exc_info=True)
        await m.reply_text(
            f"Error occoured!! {e}",
            quote=True,
        )


@DKBOTZ.on_message(filters.private & filters.command("paid_user") & filters.user(AUTH_USERS))
async def dkbotz_paiduser_admin(c, m):

    if len(m.command) == 1:
        await m.reply_text(
            "Use this command to add a user in paid bot.\n\nUsage:\n\n`/paid_user user_id user_name duration discription` ",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        paid_username = m.command[2]
        paid_duration = int(m.command[3])
        paid_reason = " ".join(m.command[4:])
        paid_log_text = f"**User Id:** {user_id}\n**User Name:** {paid_username} \n**Plan Validity:** {paid_duration} Days"  #
        try:
            await c.send_message(
                user_id,
                f"🙂 Your paid subscription started for **{paid_duration}** Days",
            )
            paid_log_text += "\n\nUser notified successfully ✅"
        except Exception as e:
            log.debug(e, exc_info=True)
            paid_log_text += f"\n\nUser notification failed !!!{e}"
        db.paid_user(user_id, paid_username, paid_duration, paid_reason)
        log.debug(paid_log_text)
        await m.reply_text(paid_log_text, quote=True)
    except Exception as e:
        log.error(e, exc_info=True)
        await m.reply_text(
            f"Error occoured!! {e}",
            quote=True,
        )


@DKBOTZ.on_message(filters.private & filters.command("paid_users") & filters.user(AUTH_USERS))
async def dkbotz_paid_usrs_admin(c, m):
    all_paid_users = db.get_all_paid_users()
    paid_usr_count = 0
    text = ""
    async for paid_user in all_paid_users:
        user_id = paid_user["id"]
        paid_duration = paid_user["paid_status"]["paid_duration"]
        paid_on = paid_user["paid_status"]["paid_on"]
        paid_username = paid_user["paid_status"]["paid_username"]
        paid_reason = paid_user["paid_status"]["paid_reason"]
        paid_usr_count += 1
        text += f"✶ **User Id** : `{user_id}`\n\n✶ **User Name** : `{paid_username}`\n\n➩ **Plan Validity** : `{paid_duration}` Days\n\n➩ **Joined On** : {paid_on} \n\n➩ **Discription** : `{paid_reason}` \n--------------------------------------------------------------\n\n"
    reply_text = f"Total Paid Users : `{paid_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        paid_usrs = io.BytesIO()
        paid_usrs.name = "paid-users.txt"
        paid_usrs.write(reply_text.encode())
        await m.reply_document(paid_usrs, True)
        return
    await m.reply_text(reply_text, True)


@DKBOTZ.on_message(filters.private & filters.command("plan_expired") & filters.user(AUTH_USERS))
async def dkbotz_plan_expireds_admin(c, m):
    if len(m.command) == 1:
        await m.reply_text(
            "Use this command to kick plan_expired user.\n\nUsage:\n\n`/plan_expired user_id`\n\n",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        plan_ex_log_text = f"Plan Validity Expired User {user_id}"

        try:
            await c.send_message(
                user_id,
                "👋 Your plan has Expired.\n\nIf you want to use the bot, You can do so by Paying.",
            )
            plan_ex_log_text += "\n\nUser notified successfully ✅"
        except Exception as e:
            log.debug(e, exc_info=True)
            plan_ex_log_text += f"\n\nUser notification failed !! {e}"
        db.remove_paid(user_id)
        log.debug(plan_ex_log_text)
        await m.reply_text(plan_ex_log_text, quote=True)
    except Exception as e:
        log.error(e, exc_info=True)
        await m.reply_text(
            f"Error occoured! {e}",
            quote=True,
        )

