from pyrogram import Client as DKBOTZ
from Config import *

app = DKBOTZ(
    "dkbotz_streamer_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="dkbotz")
)

if __name__ == "__main__":
    app.run()

