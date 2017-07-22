import json
import requests
from datetime import datetime

import secret

# Given two dates, generates a message to summarize the change in number of articles 
# since last update
def CalculateChange(oldDate, newDate):
	sign = "-" if oldDate[6] > newDate[6] else "+"
	dif = str(abs(oldDate[6] - newDate[6]))
	if dif == "0":
		prefix = "No change in number of articles in last "
	elif dif == "1":
		prefix = sign + dif + " article in last "
	else:
		prefix = sign + dif + " articles in last "

	date_hash = {
		0 : "year",
		1 : "month",
		2 : "day",
		3 : "hour",
		4 : "minute",
		5 : "second"
	}

	for i in range(6):
		if oldDate[i] != newDate[i]:
			if newDate[i] - oldDate[i] == 1:
				return prefix + date_hash[i]
			else:
				return prefix + str(newDate[i] - oldDate[i]) + " " + date_hash[i] + "s"

def ReadingSummary():
	# Get the last date as an array of ints
	last_date = []
	data = open('datafile.txt','r')
	for datum in data:
		last_date.append(int(datum.rstrip()))
	data.close()

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
		# print datetime.fromtimestamp(int(results['list'][key]['time_added']) / 1.0)
		counter += 1

	data.write(str(counter))
	data.close()
	current_date.append(counter)
	# print current_date

	print "You have " + str(counter) + " saved articles"
	change_message = CalculateChange(last_date, current_date)
	print change_message
	return 0