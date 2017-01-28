# pocket.py
# for monitoring pocket usage and updating account

import requests
import json
from Change import CalculateChange
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

	# Get the last date as an array of ints
	last_date = []
	data = open('datafile.txt','r')
	for datum in data:
		last_date.append(int(datum.rstrip()))
	data.close()
	print last_date

	# Get current date as list of ints
	current_date = list(datetime.now().timetuple()[0:6])

	# Update last date
	data = open('datafile.txt', 'w')
	for i in range(6):
		data.write(str(current_date[i]) + "\n")
	# Make request to see how many articles user has
	url = "https://getpocket.com/v3/get"
	info = {"consumer_key": secret.consumer_key, "access_token" : secret.access_token}
	res = requests.post(url, data=info)
	results = json.loads(str(res.text))
	counter = 0

	for key in results['list']:
		counter += 1

	data.write(str(counter))
	data.close()
	current_date.append(counter)
	print current_date

	print "You have " + str(counter) + " saved articles"
	change_message = CalculateChange(last_date, current_date)
	print change_message
