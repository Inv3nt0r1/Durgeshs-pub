import os
import sys
import requests
from datetime import datetime

def log_info(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] {msg}")

def log_error(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] {msg}")

log_info("Routine tunnel check script started")

# Path where your tunnel URL is saved (update if needed)
tunnel_url_path = "/home/pi/tunnel_url.txt"

# Check if tunnel URL file exists
if not os.path.isfile(tunnel_url_path):
    log_error(f"Tunnel URL file not found at {tunnel_url_path}. Cannot check tunnel status.")
    sys.exit(1)

with open(tunnel_url_path, 'r') as f:
    tunnel_url = f.read().strip()

if not tunnel_url:
    log_error("Tunnel URL is empty. Cannot check tunnel status.")
    sys.exit(1)

log_info(f"Checking tunnel URL: {tunnel_url}")

try:
    # HTTP GET request to tunnel URL with short timeout
    response = requests.get(tunnel_url, timeout=5)
    if response.status_code == 200:
        log_info("Tunnel is up and responding (HTTP 200). No action needed.")
    else:
        log_error(f"Tunnel responded with status code {response.status_code}. Rebooting RPi...")
        os.system("sudo reboot")
except Exception as e:
    log_error(f"Failed to reach tunnel URL: {e}. Rebooting RPi...")
    os.system("sudo reboot")
