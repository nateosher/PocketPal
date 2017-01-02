# pocket.py
# for monitoring pocket usage

import requests
import secret
from lxml import html

headers = {
    'Content-Type': 'application/json',
    'X-Accept': 'application/json',
}

url = "https://getpocket.com/v3/get"

info = {"consumer_key": secret.consumer_key, "access_token" : secret.access_token}

res2 = requests.post(url, data=info)

print res2.text