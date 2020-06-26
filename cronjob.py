from pyngrok.conf import PyngrokConfig
from pyngrok import ngrok
import os
import sys
import socket

import config

auth = config.auth

path = "/mnt/extdisk/Courses"
isdir = os.path.isdir(path)
if(isdir==False):
    print("[ ERROR ] Hard drive is not connected")
    sys.exit()

def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 53))
        print("[ INFO ] Network is connected.")
        return True
    except OSError:
        print("[ INFO ] Network is not connected.")
        pass
    return False

print("[ INFO ] Setting Configuration object.")
pyngrok_config = PyngrokConfig(auth_token=auth,region="in")


if(is_connected()):
    try:
        tunnels = ngrok.get_tunnels(pyngrok_config=pyngrok_config)
        print("[ INFO ] Connection was able to establish. This signifies main tunnel was absent. Restarting.")
        os.system("sudo reboot")
    except:
        print("[ INFO ] Tunnel is up.")
        sys.exit()
else:
    sys.exit()

