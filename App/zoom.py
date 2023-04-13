import jwt 
import requests
import time
import json

info = json.loads(open("App/zoom_info.json").read())

API_KEY, API_SEC = info['key'], info['secret']

def generate_token():
    token = jwt.encode(
        {"iss": API_KEY, "exp": time.time() + 5000},
        API_SEC,
        algorithm = "HS256"
    )
    return token

def generate_meeting_details():
    return {
        "topic": "Meeting",
        "type": 2,
        "start_time": "2023-07-4T10: 21: 57",
        "duration": "40",
        "timezone": "Europe/Madrid",
        "agenda": "text",
        "recurrence": {"type": 1, "repeat_interval": 1},
        "settings": {
            "host_video": "true",
            "participant_video": "true",
            "join_before_host": "False",
            "mute_upon_entry": "False",
            "watermark": "true",
            "audio": "voip",
            "auto_recording": "cloud"
        }
    }

def generate_meeting():
    headers = {
        "authorization": "Bearer " + generate_token(),
        "content-type": "application/json"
    }
    request = requests.post(f"https://api.zoom.us/v2/users/me/meetings", headers = headers,  data = json.dumps(generate_meeting_details()))
    result = json.loads(request.text)
    return (result["join_url"], result["id"], result["password"])