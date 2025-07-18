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

def get_task_status(username, password, id, product):

    params = {
        "username": username,
        "password": password,
        "id": id,
        "product": product,
        "value": "get_task",
    }

    try:
        res = requests.get("https://ytlive.dkbotzpro.in/add_online.php", params=params, timeout=15)
        response = res.json()
        
        return response
    except:
        return False


def edit_task_status(username, password, id, product, froce_stop=False, stop=False):

    params = {
        "username": username,
        "password": password,
        "id": id,
        "product": product,
        "value": "edit_task",
        "froce_stop": "true" if froce_stop else "false",
        "stop": "true" if stop else "false"
    }

    try:
        res = requests.get("https://ytlive.dkbotzpro.in/add_online.php", params=params, timeout=15)
        response = res.json()
        
        return response
    except:
        return False

