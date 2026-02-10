import requests
import time

# Load balancer URL
LOAD_BALANCER_URL = "http://localhost:5004/accounts"

# Number of requests to send
NUM_REQUESTS = 9

print("Sending requests to load balancer...\n")

for i in range(1, NUM_REQUESTS + 1):
    try:
        response = requests.get(LOAD_BALANCER_URL)
        print(f"Request {i}: Status {response.status_code}")
        print(f"→ Response from: {response.headers.get('Response-From')}")
        time.sleep(0.5)  # small delay to simulate real traffic
    except Exception as e:
        print(f"Request {i} failed: {e}")
