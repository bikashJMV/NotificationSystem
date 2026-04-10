import json
import urllib.request
from app.core.config import settings

api_key = settings.API_KEY
url = "http://localhost:8000/send/event"
data = {
    "event_name": "user.created",
    "recipient_email": "vijit@jmv.co.in",
    "data": {
        "name": "Vijit Sir"
    }
}
payload = json.dumps(data).encode("utf-8")
headers = {
    "Content-Type": "application/json",
    "X-API-Key": api_key
}

req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
print("Triggering Welcome Email...")
try:
    with urllib.request.urlopen(req) as response:
        print("Status Code:", response.status)
        print("Response Body:", response.read().decode("utf-8"))
except Exception as e:
    print(f"Error: {e}")
