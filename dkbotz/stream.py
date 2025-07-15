from pyrogram import Client as DKBOTZ, filters
from pyrogram.types import *
from Config import *
from text import *
from helpers import *





cancelled_users = set()



# /cancel cmd
@DKBOTZ.on_message(filters.command("cancel"))
async def dkbotz_cancel_handler(bot, message):
    user_id = message.from_user.id
    cancelled_users.add(user_id)
    await message.reply("❌ Setup cancelled. You Can Send /setup Again To Restart.")


async def ask(bot, message, text, is_file=False, numeric=False):
    try:
        user_id = message.from_user.id

        await bot.send_message(user_id, text)

        while True:
            response = await bot.listen(user_id)

            if response.text and response.text.lower() == "/cancel":
                cancelled_users.add(user_id)
                await bot.send_message(user_id, "❌ Setup Cancelled.")
                return False

            if numeric:
                if response.text and response.text.isdigit():
                    return int(response.text)
                else:
                    await bot.send_message(user_id, "❌ Please Enter A Valid Number (e.g., 30, 60).")
                    return False

            if is_file:
                if response.video:
                    mime_type = response.video.mime_type

                    if mime_type in ALLOWED_MIME_TYPES:
                        random_id = generate_random_string()
                        file_path = await response.download(file_name=f"{user_id}_{random_id}_video.mp4")

                        link = upload_to_bytescale(file_path, BYTESCALE_ACCOUNT_ID, BYTESCALE_PUBLIC_KEY)

                        if os.path.exists(file_path):
                            os.remove(file_path)

                        if link and check_video_link(link):
                            return link
                        else:
                            await bot.send_message(user_id, "❌ Failed to Upload Video or The Uploaded Link is Invalid.")
                            return False
                    else:
                        await bot.send_message(user_id, f"❌ Unsupported Video Format.\n\nAllowed Formats:\n- video/mp4\n- video/x-matroska")
                        return False

                elif response.text:
                    url = response.text.strip()
                    if url.startswith("http://") or url.startswith("https://"):
                        if check_video_link(url):
                            return url
                        else:
                            await bot.send_message(user_id, "❌ The link you sent is not a valid video link, or it’s in an unsupported format.")
                            return False
                    else:
                        await bot.send_message(user_id, "❌ Please Send A Valid Video Link or Upload A Video File.")
                        return False

                else:
                    await bot.send_message(user_id, "❌ Please Send A Proper <b>Video File** or a valid video link.")
                    return False

            if response.text:
                return response
            else:
                await bot.send_message(user_id, "❌ Sorry, Please Send Text Only (not stickers, photos, or documents).")
                return False

    except Exception as e:
        await message.reply(f"❌ Error: `{e}`")
        return False

# /setup cmd
@DKBOTZ.on_message(filters.command("setup"))
async def dkbotz_handle_setup(bot, message):
    user_id = message.from_user.id

    if user_id in cancelled_users:
        cancelled_users.remove(user_id)

    await bot.send_message(user_id, "🎬 <b>Stream Setup Started!**\n\nSend /cancel Anytime To Stop.")


    loop_reply = await ask(bot, message, "🔁 Do You Want To Loop The Video? (yes / no)")
    if not loop_reply:
        return

    loop_text = loop_reply.text.lower()
    loop = True if loop_text in ["yes", "y", "true", "ha", "haan"] else False


    loop_time = None
    if loop:
        loop_time_reply = await ask(bot, message, "⏱️ How Many Minutes Do You Want To Play The Video?", numeric=True)
        if loop_time_reply is False:
            return
        loop_time = loop_time_reply

    video_link = await ask(bot, message, "📥 Please Send Your <b>Video File</b> or A Direct Video Link (mp4 or mkv).", is_file=True)
    if video_link is False:
        return


    stream_url_reply = await ask(bot, message, "🌐 Please Enter Your <b>Stream URL</b>.")
    if stream_url_reply is False:
        return
    stream_url = stream_url_reply.text
    if not (stream_url.lower().startswith("rtmp://") or stream_url.lower().startswith("rtmps://")):
        await bot.send_message(user_id, f"❌ Invalid stream URL.\n\nYour URL starts with: `{stream_url.split(':')[0]}://`\nPlease send a valid RTMP URL starting with `rtmp://`.\n\nExample: `rtmp://a.rtmp.youtube.com/live2`")
        return

    stream_key_reply = await ask(bot, message, "🔑 Please Enter Your <b>Stream Key</b>.")
    if stream_key_reply is False:
        return
    stream_key = stream_key_reply.text


    if not loop_time:
        loop_time = 1000
    task_data = create_run_task(video_link, stream_url, stream_key, loop, loop_time)


    streamer = send_task_request(PREMIUM_USERNAME, PREMIUM_PASSWORD, PRODUCT_NAME, task_data)
    if streamer:
        await bot.send_message(user_id, f"✅ <b>That’s It! Your Stream Will Start Automatically in 2 minutes.</b>\n\n")
    else:
        await bot.send_message(user_id, f"❌ <b>There is No Online Server Available All Server Are Busy.</b>\n\nContact Our <b>Owner</b>: @{DEVELOPER_USERNAME}")
