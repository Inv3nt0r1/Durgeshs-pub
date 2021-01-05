from pyngrok.conf import PyngrokConfig
from pyngrok import ngrok
import os
import sys
from datetime import datetime

import config

print("Regular tunnel check script started at "+ datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

path = "/mnt/extdisk/Courses"
isdir = os.path.isdir(path)
if(isdir==False):
    print("[ ERROR ] Hard drive is not connected")
    sys.exit()

print("[ INFO ] Hard drive connected")
#print("Before auth setting")
auth = config.auth
print("[ INFO ] Auth: ",auth)
#ngrok.set_auth_token(auth)
pyngrok_config = PyngrokConfig(auth_token=auth,region="in")
print("[ INFO ] Auth and region set done")
#public_url = ngrok.connect()
public_url = ngrok.connect(8096,pyngrok_config=pyngrok_config)
print("[ INFO ] connect is done")
public_url = "https"+public_url[4:]
print("[ INFO ] URL: ",public_url)



with open('/home/pi/Durgeshs-pub/redirect.js','r') as file:
    data = file.readlines()

data[0] = 'var link = "'+public_url+'"\n'

with open('/home/pi/Durgeshs-pub/redirect.js','w') as file:
    file.writelines(data)

#print("\n\n\nData: ",data,"\n\n\n")
"""
os.system("cd /home/pi/Durgeshs-pub")
os.system("git add .")
os.system("git commit -m 'This commit is automatically done by the server script, to keep updating the reverse proxy tunnel'")
os.system("git push")
"""
