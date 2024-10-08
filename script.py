from pyngrok.conf import PyngrokConfig
from pyngrok import ngrok
import os
import sys
from datetime import datetime
import subprocess

import config

print("Reboot python script started at "+ datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

# Mounting the hard disk partitions
os.system("sudo mount /dev/sda5 /mnt/ExtDiskNas")
os.system("sudo mount /dev/sda1 /mnt/NextCloudDriveMountPoint")

path = "/mnt/ExtDiskNas/Learnings"
isdir = os.path.isdir(path)
if(isdir==False):
    print("[ ERROR ] Hard drive is not connected")
    sys.exit()


cmd = '''
while true; do 
 ssh -p 443 -R0:localhost:8096 -o StrictHostKeyChecking=no -o ServerAliveInterval=30 gF3kJEuV3JW@a.pinggy.io ; 
sleep 10; done
'''
subprocess.check_output(cmd, shell=True)


# print("[ INFO ] Hard drive connected")
# #print("Before auth setting")
# auth = config.auth

# ngrok.set_auth_token(auth)
# pyngrok_config = PyngrokConfig(auth_token=auth,region="in")
# #pyngrok_config = PyngrokConfig(auth_token=auth)

# print("[ INFO ] Auth and region set done")
# #public_url = ngrok.connect()
# public_url = ngrok.connect(8096,pyngrok_config=pyngrok_config).public_url
# print("[ INFO ] connect is done")
# print("[ INFO ] URL: ",public_url)

# with open('/home/pi/Durgeshs-pub/redirect.js','r') as file:
#     data = file.readlines()

# data[0] = 'var link = "'+public_url+'/web/'+'"\n'

# with open('/home/pi/Durgeshs-pub/redirect.js','w') as file:
#     file.writelines(data)


# os.chdir("/home/pi/Durgeshs-pub")
# os.system("cd /home/pi/Durgeshs-pub")
# os.system("git pull")
# os.system("git add .")
# os.system("git commit -m 'This commit is automatically done by the server script, to keep updating the reverse proxy tunnel'")
# os.system("git push")

# print("[ INFO ] Done pushing the updated link. Holding on the process for ngrok :)")

# ngrok_process = ngrok.get_ngrok_process()

# try:
#     # Block until CTRL-C or some other terminating event
#     ngrok_process.proc.wait()
# except KeyboardInterrupt:
#     print(" Shutting down server.")

#     ngrok.kill()

#print("\n\n\nData: ",data,"\n\n\n")

