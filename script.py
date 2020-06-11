from pyngrok.conf import PyngrokConfig
from pyngrok import ngrok
import os

import config

print("Before auth setting")
auth = config.auth
print("Auth: ",auth)
#ngrok.set_auth_token(auth)
pyngrok_config = PyngrokConfig(auth_token=auth)
print("Auth set done")
pyngrok_config = PyngrokConfig(region="in")
print("region set done")
#public_url = ngrok.connect()
public_url = ngrok.connect(8096,pyngrok_config=pyngrok_config)
print("connect is also done")
print("URL: ",public_url)

with open('redirect.js','r') as file:
    data = file.readlines()

data[0] = 'var link = "'+public_url+'"\n'
print(data)

with open('redirect.js','w') as file:
    file.writelines(data)

print("\n\n\nData: ",data,"\n\n\n")

os.system("cd ~/Desktop/Durgeshs-pub")
os.system("git add .")
os.system("git commit -m 'This commit is automatically done by the server script, to keep updating the reverse proxy tunnel'")
os.system("git push")

