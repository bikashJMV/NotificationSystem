import os
import json
import urllib.request
from app.config import settings

api_key = settings.API_KEY
url = "http://localhost:8000/send/event"
data = {
    "event_name": "asset.assigned",
    "recipient_email": "vijit@jmv.co.in",
    "data": {
        "name": "Vijit Sir",
        "asset_name": "Dell XPS 15",
        "asset_model": "9520",
        "serial_number": "DXPS123",
        "assigned_date": "2026-04-09"
    }
}
payload = json.dumps(data).encode("utf-8")
headers = {
    "Content-Type": "application/json",
    "X-API-Key": api_key
}

req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
print(f"Triggering email dispatch to {url}...")
try:
    with urllib.request.urlopen(req) as response:
        print("Status Code:", response.status)
        print("Response Body:", response.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
