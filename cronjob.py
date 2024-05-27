from pyngrok.conf import PyngrokConfig
from pyngrok import ngrok
import os
import sys
import socket
from datetime import datetime
import config

print("Routine tunnel check script started at "+ datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

# ------- Checking the Hard Drive Connection and MountPoint -------------
path = "/mnt/ExtDiskNas/Learnings"
isdir = os.path.isdir(path)
if(isdir==False):
    print("[ ERROR ] Hard drive is not connected")
    try:
        # Mounting the hard disk partitions
        print("[ INFO ] Attempting to mount the partitions")
        os.system("sudo mount /dev/sda1 /mnt/ExtDiskNas")
        os.system("sudo mount /dev/sda2 /mnt/NextCloudDriveMountPoint")
    except:
        os.system("[ ERROR ] Attempt Failed. Please check the drive!")
        sys.exit()
    

# -------- Checking the Network Connection ------------------------------
REMOTE_SERVER = "one.one.one.one"
def is_connected(hostname):
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False


# ------------ Testing the Reverse Proxy Tunnel ---------------------------
auth = config.auth

ngrok.set_auth_token(auth)
print("[ INFO ] Setting Configuration object.")
pyngrok_config = PyngrokConfig(auth_token=auth,region="in")
#pyngrok_config = PyngrokConfig(auth_token=auth)

if(is_connected(REMOTE_SERVER)):
    try:
        tunnels = ngrok.get_tunnels(pyngrok_config=pyngrok_config)
        print("[ INFO ] Connection was able to establish. This signifies main tunnel was absent. Restarting.")
        os.system("sudo reboot")
    except:
        print("[ INFO ] Tunnel is up.")
        sys.exit()
else:
    sys.exit()

