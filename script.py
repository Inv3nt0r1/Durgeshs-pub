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
