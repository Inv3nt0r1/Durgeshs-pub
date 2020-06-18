from pyngrok.conf import PyngrokConfig
from pyngrok import ngrok
import os
import sys
import socket

import config

auth = config.auth

def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False

pyngrok_config = PyngrokConfig(auth_token=auth,region="in")

if(is_connected()):
    try:
        tunnels = ngrok.get_tunnels(pyngrok_config=pyngrok_config)
        os.system("sudo reboot")
    except:
        sys.exit()
else:
    sys.exit()

