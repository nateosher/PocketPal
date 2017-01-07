# pocket.py
# for monitoring pocket usage and updating account

import requests
import json
from os import path

headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'X-Accept': 'application/json',
}

if not path.isfile("secret.py"):
	from PocketInit import PocketInitialize
	print "No account detected."
	key = raw_input("Please enter your product key: ")
	PocketInitialize(key,headers)
else:
	import secret

	f = open('datafile.txt','w')
	url = "https://getpocket.com/v3/get"
	info = {"consumer_key": secret.consumer_key, "access_token" : secret.access_token}
	res = requests.post(url, data=info)
	results = json.loads(str(res.text))
	counter = 0

	for key in results['list']:
		counter += 1

	print "You have " + str(counter) + " saved articles"
