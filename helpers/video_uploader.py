import requests

# Bytescale : Create Account with Fake Mail. You Will Get 10GB Free Stroage 
def upload_to_bytescale(file_path, account_id, public_key):
    url = f"https://api.bytescale.com/v2/accounts/{account_id}/uploads/binary"
    headers = {
        "Authorization": f"Bearer {public_key}",
        "Content-Type": "video/mp4"
    }

    try:
        with open(file_path, "rb") as f:
            response = requests.post(url, headers=headers, data=f)

        if response.status_code == 200:
            json_data = response.json()
            file_url = json_data.get("fileUrl")
            print(f"✅ Upload successful! File URL: {file_url}")
            return file_url
        else:
            print(f"❌ Upload failed! Status Code: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return None
