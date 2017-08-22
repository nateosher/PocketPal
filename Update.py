import json
import requests
from datetime import datetime

import secret

# Given two dates, generates a message to summarize the change in number of articles 
# since last update
def CalculateChange(oldDate, newDate):
	sign = "-" if oldDate[6] > newDate[6] else "+"
	savedDif = str(abs(oldDate[6] - newDate[6]))
	readDif = str(abs(oldDate[7] - newDate[7]))
	if savedDif == "0":
		prefix = "No change in number of articles"
	elif savedDif == "1":
		prefix = sign + savedDif + " article saved and " + readDif + " read"
	else:
		prefix = sign + savedDif + " articles saved and " + readDif + " read"

	prefix = prefix + " in last "

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

# Summary of how much you've read recently
def ReadingSummary(poc):
	# Get the last date as an array of ints
	last_date = []
	data = open('data/datafile.txt','r')
	for datum in data:
		last_date.append(int(datum.rstrip()))
	data.close()

	# Get current date as list of ints
	current_date = list(datetime.now().timetuple()[0:6])
	# Make request to see how many articles user has
	try:
		results = poc.get_saved()
	except:
		print "\033[1mError\033[0m- check internet connection and try again"
		return 0
	try:
		readArts = poc.get_archived()
	except:
		print "\033[1mError\033[0m- check internet connection and try again"
		return 0

	# Update last date
	data = open('data/datafile.txt', 'w')
	for i in range(6):
		data.write(str(current_date[i]) + "\n")
	# Get number of saved articles
	counter = len(list(results.keys()))
	numRead = len(list(readArts.keys()))

	data.write(str(counter)+"\n")
	data.write(str(numRead))
	data.close()
	current_date.append(counter)
	current_date.append(numRead)

	print "You have " + str(counter) + " saved articles"
	print "You have read " + str(numRead) + " articles"
	change_message = CalculateChange(last_date, current_date)
	print change_message

	return 0

# Cleans up old articles that are just collecting dust
def CleanUp(poc):
	# convert cutoff date to actual date
	while True:
		cutoffDate = raw_input(("Please enter cutoff date for "
			"removal (mm/dd/yyyy):\n>> "))
		if cutoffDate == "":
			print "Action canceled"
			return 0
		try:
			cutoffDate = datetime.strptime(cutoffDate, "%m/%d/%Y")
			break
		except ValueError:
			print "Format error- be sure to pad month and day with 0's if necessary"
			print "Enter empty string to cancel action"
	print "Retrieving saved articles..."
	try:
		saved = poc.get_saved()
	except:
		print "\033[1mError\033[0m- check internet connection and try again"
		return 0
	count = 0
	for key in saved.keys():
		# TODO: Make deletion more robust (check status, etc.)
		curTime = datetime.fromtimestamp(float(saved[key]['time_added']))
		curID = int(saved[key]['item_id'])
		if curTime < cutoffDate:
			count += 1
			print 'Found article: "' + saved[key]['resolved_title'] + '"'
			while True:
				resp = raw_input(("Would you like to delete, archive, "
					"or neither? (d/a/n):\n>> "))
				if resp == "d":
					try:
						poc.delete(curID)
						print "Article deleted"
						break
					except:
						print ("\033[1mError\033[0m- check internet "
							"connection and try again")
						return 0
				elif resp == "a":
					try:
						poc.archive(curID)
						print "Article archived"
						break
					except:
						print ("\033[1mError\033[0m- check internet "
							"connection and try again")
						return 0
				elif resp == "n" or resp == "":
					print "Article will remain in saved"
					break
				else:
					print "Command not recognized"
	if count == 0:
		print "No articles added before this date"
	return 0

if __name__ == '__main__':
	from Pocket import Pocket
	import secret
	poc = Pocket(secret.consumer_key, secret.access_token)
	CleanUp(poc)




