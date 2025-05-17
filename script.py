import subprocess
import re
import os
import sys
from datetime import datetime

def log_info(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] {msg}")

def log_error(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] {msg}")

def log_warning(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [WARNING] {msg}")

def start_tunnel_and_get_url():
    log_info("Starting cloudflared tunnel...")
    
    try:
        proc = subprocess.Popen(
            ["/usr/local/bin/cloudflared", "tunnel", "--url", "http://localhost:8096"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
    except Exception as e:
        log_error(f"Failed to start cloudflared: {e}")
        sys.exit(1)

    tunnel_url = None
    log_info("Reading cloudflared output to capture the tunnel URL...")

    for line in proc.stdout:
        line = line.strip()
        print(f"[cloudflared] {line}")

        # Match the tunnel URL line
        match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
        if match:
            tunnel_url = match.group(0)
            log_info(f"Tunnel URL detected: {tunnel_url}")
            break

    if not tunnel_url:
        log_error("Could not find tunnel URL in cloudflared output.")
        proc.terminate()
        raise RuntimeError("Tunnel URL not found in cloudflared output.")

    log_info("Tunnel successfully started.")
    return tunnel_url, proc

def save_url_to_file(public_url, url_file_path="/home/pi/Durgeshs-pub/tunnel_url.txt"):
    log_info(f"Saving tunnel URL to {url_file_path}...")
    try:
        with open(url_file_path, "w") as f:
            f.write(public_url)
        log_info(f"Tunnel URL saved to {url_file_path}: {public_url}")
    except Exception as e:
        log_error(f"Failed to save URL to file: {e}")
        raise

def update_redirect_js(public_url, redirect_js_path="/home/pi/Durgeshs-pub/redirect.js"):
    log_info(f"Updating redirect.js with new URL: {public_url}...")
    try:
        with open(redirect_js_path, 'r') as file:
            data = file.readlines()

        # Update first line with new URL (adjust if needed)
        data[0] = f'var link = "{public_url}/web/"\n'

        with open(redirect_js_path, 'w') as file:
            file.writelines(data)

        log_info(f"redirect.js successfully updated with new URL.")
    except FileNotFoundError:
        log_warning(f"redirect.js not found at {redirect_js_path}. Skipping update.")
    except Exception as e:
        log_error(f"Failed to update redirect.js: {e}")
        raise

def git_push_changes(repo_path="/home/pi/Durgeshs-pub"):
    log_info(f"Navigating to repo path: {repo_path}")
    try:
        os.chdir(repo_path)
        log_info("Pulling latest changes...")
        os.system("git pull")

        log_info("Adding changes to git...")
        os.system("git add .")

        log_info("Committing changes...")
        os.system('git commit -m "Auto update tunnel URL"')

        log_info("Pushing changes to remote...")
        os.system("git push")

        log_info("Changes successfully pushed to GitHub.")
    except Exception as e:
        log_error(f"Git push failed: {e}")
        raise

def main():
    try:
        log_info("Starting tunnel creation and URL update process.")
        public_url, tunnel_proc = start_tunnel_and_get_url()

        # Save URL to file
        save_url_to_file(public_url)

        # Update redirect.js
        update_redirect_js(public_url)

        # Git push
        git_push_changes()

        log_info("Tunnel setup complete. Holding the process to keep the tunnel alive...")
        # Wait here to keep tunnel process alive
        tunnel_proc.wait()

    except Exception as e:
        log_error(f"Startup script encountered an error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
