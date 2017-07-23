# pocket.py
# for monitoring pocket usage and updating account

# Core packages
import requests
import json
from os import path

# Custom methods
from Update import ReadingSummary

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
	while True:
		next = raw_input("What would you like to do next? (q for quit, o for options)\n")
		if next == "q" or next == "quit":
			break
		if next == "o":
			print """q or quit     -> quits application
r or reading  -> Gives summary of your recent reading
s or scrape   -> Check to see if your favorite sites have put out any new Content (IN PROGRESS)
f or favorite -> Update your "favorite" sites (IN PROGRESS)
c or clean    -> Remove articles added before a certain date, or a certain amount of time ago (IN PROGRESS)
			"""
		if next == "r" or next == "reading":
			ReadingSummary()
		else:
			print "Unknown or unsupported command"

