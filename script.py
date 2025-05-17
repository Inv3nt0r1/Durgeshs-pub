import subprocess
import re
import os
import sys
from datetime import datetime

def log_info(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] {msg}")

def log_error(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] {msg}")

def start_tunnel_and_get_url():
    log_info("Starting cloudflared tunnel...")
    proc = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", "http://localhost:8096"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    tunnel_url = None

    for line in proc.stdout:
        line = line.strip()
        print(f"[cloudflared] {line}")
        match = re.search(r"HTTP URL:\s*(https?://\S+)", line)
        if match:
            tunnel_url = match.group(1)
            log_info(f"Tunnel URL found: {tunnel_url}")
            break

    if not tunnel_url:
        proc.terminate()
        raise RuntimeError("Could not find tunnel URL in cloudflared output")

    return tunnel_url, proc

def update_redirect_js(public_url, redirect_js_path="/home/pi/Durgeshs-pub/redirect.js"):
    try:
        with open(redirect_js_path, 'r') as file:
            data = file.readlines()

        # Update first line with new URL (adjust if needed)
        data[0] = f'var link = "{public_url}/web/"\n'

        with open(redirect_js_path, 'w') as file:
            file.writelines(data)

        log_info(f"Updated redirect.js with new URL: {public_url}")
    except Exception as e:
        log_error(f"Failed to update redirect.js: {e}")
        raise

def git_push_changes(repo_path="/home/pi/Durgeshs-pub"):
    try:
        os.chdir(repo_path)
        os.system("git pull")
        os.system("git add .")
        os.system('git commit -m "Auto update tunnel URL"')
        os.system("git push")
        log_info("Committed and pushed updated URL to GitHub repo")
    except Exception as e:
        log_error(f"Git push failed: {e}")
        raise

def main():
    try:
        public_url, tunnel_proc = start_tunnel_and_get_url()

        # Save URL to file in Durgeshs-pub folder
        url_file_path = "/home/pi/Durgeshs-pub/tunnel_url.txt"
        with open(url_file_path, "w") as f:
            f.write(public_url)
        log_info(f"Saved tunnel URL to {url_file_path}")

        # Update redirect.js
        update_redirect_js(public_url)

        # Git push
        git_push_changes()

        log_info("Tunnel setup complete. Waiting to keep tunnel alive...")
        # Wait here to keep tunnel process alive
        tunnel_proc.wait()

    except Exception as e:
        log_error(f"Startup tunnel script failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
