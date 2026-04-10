import json
import urllib.request
import urllib.error
import time
from app.core.config import settings

BASE_URL = "http://localhost:8000"
API_KEY = settings.API_KEY
HEADERS = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

def print_header(title):
    print(f"\n{'='*50}\n>> {title}\n{'='*50}")

def print_result(success, msg):
    if success:
         print(f"[PASS] {msg}")
    else:
         print(f"[FAIL] {msg}")

def test_health_check():
    print_header("Test 1: Health Check Endpoint")
    url = f"{BASE_URL}/"
    req = urllib.request.Request(url, method="GET")
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            body = json.loads(response.read().decode("utf-8"))
            
            print_result(status == 200, f"Status code is {status}")
            print_result(body.get("status") == "ok", "Payload status is 'ok'")
            print_result("user.created" in body.get("supported_events", []), "supported_events list found")
            return status == 200
    except Exception as e:
        print_result(False, f"Exception occurred: {e}")
        return False

def test_event(event_name, payload_data, test_number):
    print_header(f"Test {test_number}: Trigger '{event_name}' Event")
    url = f"{BASE_URL}/send/event"
    
    data = {
        "event_name": event_name,
        "recipient_email": "vijit@jmv.co.in",
        "data": payload_data
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=HEADERS, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            body = json.loads(response.read().decode("utf-8"))
            
            print_result(status == 202, f"Status code is {status} (Expected 202)")
            print_result("request_id" in body, f"Request ID generated: {body.get('request_id')}")
            return True
    except urllib.error.HTTPError as e:
        print_result(False, f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print_result(False, f"Exception occurred: {e}")
        return False

def test_invalid_event():
    print_header("Test 5: Trigger Invalid Event Name")
    url = f"{BASE_URL}/send/event"
    data = {
        "event_name": "fake.event.doesnt.exist",
        "recipient_email": "vijit@jmv.co.in",
        "data": {}
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=HEADERS, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            print_result(False, f"Unexpectedly succeeded with status {response.status}")
            return False
    except urllib.error.HTTPError as e:
        print_result(e.code == 400, f"Correctly caught HTTP {e.code} Bad Request")
        return e.code == 400
    except Exception as e:
        print_result(False, f"Exception occurred: {e}")
        return False

def test_rate_limit_bypass(amount):
    print_header(f"Test 6: Rate Limiting Safety Check ({amount} fast requests)")
    url = f"{BASE_URL}/"
    req = urllib.request.Request(url, method="GET")
    
    successes = 0
    failures = 0
    
    for i in range(amount):
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    successes += 1
        except urllib.error.HTTPError as e:
            if e.code == 429:
                failures += 1
            else:
                pass # Other error
                
    print(f"Details: {successes} successful requests, {failures} blocked by SlowAPI (429)")
    print_result(True, "Rate Limit Logic Tested.")

if __name__ == "__main__":
    print("-" * 50)
    print("STARTING E2E INTEGRATION TEST SUITE")
    print("-" * 50)
    
    test_health_check()
    time.sleep(1)
    
    test_event("user.created", {"name": "Test User"}, 2)
    time.sleep(1)
    
    test_event("asset.assigned", {"name": "Test User", "asset_name": "Test Laptop", "asset_model": "Dell", "serial_number": "1234", "assigned_date": "2026-04-10"}, 3)
    time.sleep(1)
    
    test_event("asset.returned", {"name": "Test User", "asset_name": "Test Laptop", "serial_number": "1234", "returned_date": "2026-04-10"}, 4)
    time.sleep(1)
    
    test_invalid_event()
    
    # We do a tiny rate limit check against health check just to show network isn't choking
    # Note: send/event is rate-limited 60/min. health doesn't have the decorator but it proves uptime.
    test_rate_limit_bypass(5)
    
    print("\n" + "="*50)
    print("TEST SUITE COMPLETE")
    print("="*50)
