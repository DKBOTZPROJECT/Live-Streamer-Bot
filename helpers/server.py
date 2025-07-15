from urllib.parse import quote
import requests, json

rtmp_urls = {
    "YouTube": "rtmp://a.rtmp.youtube.com/live2",
    "Facebook": "rtmp://live-api-s.facebook.com:80/rtmp/",
}



def send_task_request(username, password, product, task_data):
    encoded_data = json.dumps(task_data)
    
    params = {
        "username": username,
        "password": password,
        "product": product,
        "value": "add_task",
        "data": encoded_data
    }

    try:
        res = requests.get("https://ytlive.dkbotzpro.in/add_task.php", params=params, timeout=15)
        response = res.json()
        return response['status']
    except:
        return False


def create_run_task(file_link, rtmp_url, rtmp_key, loop=True, stop_time=1000):
    task = {
        "task": "run",
        "file_link": file_link,
        "loop": loop,
        "stop_time": stop_time,
        "rtmp_url": rtmp_url,
        "rtmp_key": rtmp_key
    }
    return task
