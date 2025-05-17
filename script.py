import os
import sys
import subprocess
from datetime import datetime

# Paths
MOUNT_PATH_1 = "/mnt/ExtDiskNas"
MOUNT_PATH_2 = "/mnt/NextCloudDriveMountPoint"
REDIRECT_JS_PATH = "/home/pi/Durgeshs-pub/redirect.js"
URL_FILE_PATH = "/home/pi/Durgeshs-pub/tunnel_url.txt"
GIT_REPO_PATH = "/home/pi/Durgeshs-pub"
CLOUDFLARED_PATH = "/usr/local/bin/cloudflared"

# Hard Drive Partitions
PARTITION_1 = "/dev/sda5"
PARTITION_2 = "/dev/sda1"

def log(message, level="INFO"):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [{level}] {message}")

def mount_drives():
    log("Checking hard drive connection...")
    
    # Check if specific folder is accessible
    learnings_path = "/mnt/ExtDiskNas/Learnings"
    if not os.path.isdir(learnings_path):
        log(f"{learnings_path} is not accessible. Attempting to mount...", "ERROR")
        
        log(f"Mounting {PARTITION_1} to {MOUNT_PATH_1}...")
        os.system(f"sudo mount {PARTITION_1} {MOUNT_PATH_1}")
        
        log(f"Mounting {PARTITION_2} to {MOUNT_PATH_2}...")
        os.system(f"sudo mount {PARTITION_2} {MOUNT_PATH_2}")
    
    # Verify Mount
    if os.path.isdir(learnings_path):
        log(f"Successfully mounted {MOUNT_PATH_1}.")
    else:
        log(f"Failed to mount {MOUNT_PATH_1}.", "ERROR")
        sys.exit()


import re

def start_tunnel():
    log("Starting cloudflared tunnel...")

    try:
        log(f"Executing command: {CLOUDFLARED_PATH} tunnel --url http://localhost:8096")
        proc = subprocess.Popen(
            [CLOUDFLARED_PATH, "tunnel", "--url", "http://localhost:8096"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        public_url = None
        log("Waiting for tunnel URL...")

        url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

        for line in proc.stdout:
            log(f"[CLOUDFLARED] {line.strip()}")

            # Extract URL using regex
            url_match = url_pattern.search(line)
            if url_match:
                public_url = url_match.group(0)
                log(f"Tunnel URL obtained: {public_url}")
                break

        if not public_url:
            log("[ERROR] Failed to extract the tunnel URL.", "ERROR")
            proc.terminate()
            sys.exit()

        # Save the URL to a file
        log(f"Saving URL to {URL_FILE_PATH}...")
        with open(URL_FILE_PATH, "w") as url_file:
            url_file.write(public_url)

        # Update the redirect.js file
        update_redirect_js(public_url)

        # Push changes to GitHub
        push_to_github()

    except Exception as e:
        log(f"[ERROR] Error starting cloudflared: {str(e)}", "ERROR")
        sys.exit()


def update_redirect_js(public_url):
    try:
        log(f"Updating redirect.js file at {REDIRECT_JS_PATH} with the new URL...")
        with open(REDIRECT_JS_PATH, 'r') as file:
            data = file.readlines()

        new_link = f'var link = "{public_url}/web/"\n'
        data[0] = new_link

        with open(REDIRECT_JS_PATH, 'w') as file:
            file.writelines(data)

        log(f"Successfully updated redirect.js with new link: {new_link.strip()}")
    except Exception as e:
        log(f"Failed to update redirect.js: {str(e)}", "ERROR")

def push_to_github():
    try:
        log("Navigating to GitHub repository...")
        os.chdir(GIT_REPO_PATH)

        log("Pulling latest changes...")
        os.system("git pull")

        log("Adding changes to the staging area...")
        os.system("git add .")

        log("Committing changes...")
        os.system("git commit -m 'Auto-update redirect link'")

        log("Pushing changes to GitHub...")
        os.system("git push")
        log("Successfully pushed changes to GitHub.")
    except Exception as e:
        log(f"Failed to push changes to GitHub: {str(e)}", "ERROR")

def main():
    log("Reboot script started.")
    mount_drives()
    start_tunnel()
    log("Reboot script completed.")

if __name__ == "__main__":
    main()
