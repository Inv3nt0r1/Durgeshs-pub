from pyngrok.conf import pyngrokConfig
from pyngrok import ngrok
import os

import config

auth = config.auth
ngrok.set_auto_token(auth)
pyngrok_config = PyngrokConfig(region="in")

public_url = ngrok.connect(80)
print("URL: ",public_url)