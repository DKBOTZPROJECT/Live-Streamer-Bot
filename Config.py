import os, re
from os import environ


API_ID = int(environ.get("API_ID", "1234567"))
API_HASH = environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = environ.get("BOT_TOKEN", "your_bot_token")



# Info 
CHANNEL_USERNAME = environ.get("CHANNEL_USERNAME", "DKBOTZ")
DEVELOPER_USERNAME = environ.get("DEVELOPER_USERNAME", "DKBOTZPRO")

# Payment Method
QR_IMAGE_URL = environ.get("QR_IMAGE_URL", "https://premium.dkbotzpro.in/QR.jpg")
UPI_ID = environ.get("UPI_ID", "dkbotz@ybl")
CRYPTO = environ.get("CRYPTO", "Contact To @DKBOTZHELP")
PAYTM = environ.get("PAYTM", "dkbotz@ybl")
PHONEPE = environ.get("PHONEPE", "dkbotz@ybl")
PAYPAL = environ.get("PAYPAL", "Contact To @DKBOTZHELP")


# premium.dkkbotzpro.in Account Details
PREMIUM_USERNAME = environ.get("PREMIUM_USERNAME", "")
PREMIUM_PASSWORD = environ.get("PREMIUM_PASSWORD", "")
PRODUCT_NAME = "Traffic-Tool-V1"


# Video Uploaser
BYTESCALE_ACCOUNT_ID = environ.get("BYTESCALE_ACCOUNT_ID", "")
BYTESCALE_PUBLIC_KEY = environ.get("BYTESCALE_PUBLIC_KEY", "")


# Don't Edit
ALLOWED_MIME_TYPES = ['video/mp4', 'video/x-matroska']
