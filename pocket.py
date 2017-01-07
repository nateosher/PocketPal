# pocket.py
# for monitoring pocket usage and updating account

import requests
import json
from datetime import datetime
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

	last_date = []
	data = open('datafile.txt','r')
	for datum in data:
		last_date.append(datum.rstrip())
	data.close()
	print last_date
	current_date = list(datetime.now().timetuple()[0:6])
	print current_date
	data = open('datafile.txt', 'w')
	for i in range(0,6):
		data.write(str(current_date[i]) + "\n")
	url = "https://getpocket.com/v3/get"
	info = {"consumer_key": secret.consumer_key, "access_token" : secret.access_token}
	res = requests.post(url, data=info)
	results = json.loads(str(res.text))
	counter = 0

	for key in results['list']:
		counter += 1

	print "You have " + str(counter) + " saved articles"
