import requests
import os
import random
import string


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

  
