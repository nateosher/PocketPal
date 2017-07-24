# pocket.py
# for monitoring pocket usage and updating account

# Core packages
import requests
import json
from os import path

# Custom methods
import secret
from Update import ReadingSummary
from Reader import AddFavorites, UpdateArticles, ViewFavorites
from Pocket import Pocket

if not path.isfile("secret.py"):
	from PocketInit import PocketInitialize
	print "No account detected."
	key = raw_input("Please enter your product key: ")
	PocketInitialize(key)
else:
	poc = Pocket(secret.consumer_key, secret.access_token)
	while True:
		next = raw_input("What would you like to do next? (q for quit, o for options): ")
		if next == "q" or next == "quit":
			break
		elif next == "o":
			print """q or quit     -> quits application
s or summary  -> Gives summary of your recent reading
sc or scrape   -> Check to see if your favorite sites have put out any new Content
f or favorites -> Update your "favorite" sites
vf or view    -> List favorite sites
c or clean    -> Remove articles added before a certain date, or a certain amount of time ago (IN PROGRESS)
			"""
		elif next == "s" or next == "summary":
			ReadingSummary()
		elif next == "f" or next == "favorites":
			AddFavorites()
		elif next == "sc" or next == "scrape":
			UpdateArticles(poc)
		elif next == "vf" or next == "view":
			ViewFavorites()
		else:
			print "Unknown or unsupported command"

