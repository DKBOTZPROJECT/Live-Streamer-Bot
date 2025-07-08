from pyrogram import Client as DKBOTZ, filters
from pyrogram.types import *
from Config import *

START_MESSAGE = """🎥 <b>Welcome To The YouTube Live Streamer Bot!</b>

✨ I Am Here To Help You Stream <b>24/7 Videos</b> On:
🔴 <b>YouTube
🔵 Facebook
🟣 And Many Other Platforms!</b>

💡 Whether You Are A Creator, Brand, Or Business, I Will Make Your <b>Live Streaming</b> Easy And Non-Stop For You.

ℹ️ <b>Want To Know More?</b> 
👉 Tap The Buttons Below!
"""

def start_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("💰 Plans", callback_data="plans"),
                InlineKeyboardButton("ℹ️ Help", callback_data="help")
            ],
            [
                InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{DEVELOPER_USERNAME}"),
                InlineKeyboardButton("📢 Channel", url=f"https://t.me/{CHANNEL_USERNAME}")
            ]
        ]
    )



HELP_MESSAGE = """
👋 <b>Hello Dear User!</b>

I Am A Powerful Bot That Helps You Stream <b>24/7 Videos</b> Without Any Break On Platforms Like:

🔴 <b>YouTube</b>  
🔵 <b>Facebook</b>  
🟣 <b>And Other Streaming Sites</b>

<b>✨ What I Can Do:</b>  
✅ Stream Videos 24/7 Automatically  
✅ Run Live Streams For Personal, Brand, Or Business Use  
✅ Schedule And Manage Your Broadcasts Easily  
✅ Offer Budget-Friendly Streaming Plans

<b>💳 Payment Methods Supported:</b>  
✔️ UPI  
✔️ Paytm  
✔️ PhonePe  
✔️ Crypto (BTC / USDT)  
✔️ PayPal  
✔️ Credit / Debit Cards

<b>📝 How To Start:</b>  
1️⃣ Use /plan To View Available Plans  
2️⃣ Tap <b>Buy Now</b> To Get Payment Info  
3️⃣ Complete The Payment And Send Screenshot To Developer  
4️⃣ Your Stream Will Be Activated Shortly!

<b>⚙️ How To Setup Live Stream:</b>  
- Send <code>/setup</code>  
- It Will Ask: <b>"Do You Want To Loop The Video?"</b>  
- Then Send The Video File  
- Then Send Your <b>Stream Key</b>  
✅ That’s It! Your Stream Will Start Automatically

<b>🛑 To Stop Live:</b>  
- Send <code>/stop</code> – To Gracefully Stop The Stream  
- Send <code>/force_stop</code> – To Force Stop Immediately

<b>✅ Available Commands:</b>  
/start – Show Welcome Message  
/help – Show This Help Guide  
/plan – View Plans And Pricing  
/setup – Start Your Live Stream  
/stop – Stop Streaming Safely  
/force_stop – Force Stop Live Immediately

👇 Tap The Buttons Below To Continue!
"""


def dkbotz_help_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🏠 Home", callback_data="home"),
                InlineKeyboardButton("💰 Plans", callback_data="plans")
            ],
            [
                InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{DEVELOPER_USERNAME}"),
                InlineKeyboardButton("📢 Channel", url=f"https://t.me/{CHANNEL_USERNAME}")
            ]
        ]
    )




PLAN_DETAILS_TEXT = """
💰 <b>Our Streaming Plans</b>

🎬 <b>Plan List:</b>
▫️ <b>24 Hours (1 Day)</b> — ₹19 Only
▫️ <b>1 Week</b> — ₹119 Only
▫️ <b>1 Month</b> — ₹499 Only
▫️ <b>2 Months</b> — ₹899 Only
▫️ <b>3 Months</b> — ₹1,299 Only

💳 <b>Payment Methods:</b>
✅ UPI (All Apps Supported)
✅ Crypto Currency (BTC / USDT etc.)
✅ QR Code
✅ Paytm
✅ PhonePe
✅ PayPal
✅ Credit / Debit Card

📝 <b>Note:</b> After Payment, Please Send Payment Screenshot To Developer.

👇 Tap Buy Now To Get Payment Details!
"""




def dkbotz_plan_buttons():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🛒 Buy Now", callback_data="buy_now")],
            [
                InlineKeyboardButton("🏠 Home", callback_data="home"),
                InlineKeyboardButton("ℹ️ Help", callback_data="help")],
            [
                InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{DEVELOPER_USERNAME}")
            ]
        ]
    )


