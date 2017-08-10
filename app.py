# pocket.py
# for monitoring pocket usage and updating account

# Core packages
import requests
import json
import os

# Custom methods
import data.secret as secret
from Update import ReadingSummary, CleanUp
from Reader import AddFavorites, UpdateArticles, ViewFavorites
from Pocket import Pocket
from Stats import ReadingStats
from Roll import RandomArticle
from NewsAPI import Aggregator

# TODO: Implement some form of cacheing for pocket object and NewsAPI object

# Set running directory to current directory of the script
CURRENT_DIRECTORY = os.path.dirname(__file__)
if CURRENT_DIRECTORY:
	os.chdir(CURRENT_DIRECTORY)

# Check to see if everything is all set up
if not os.path.isfile("data/secret.py"):
	from PocketInit import PocketInitialize
	PocketInitialize()
else:
	# TODO: Aggregator initialize
	poc = Pocket(secret.consumer_key, secret.access_token)
	agg = Aggregator(secret.news_api_key)
	while True:
		next = raw_input("What would you like to do next? (q for quit, o for options): ")
		if next == "q" or next == "quit":
			os.system('clear')
			break
		elif next == "o":
			os.system('clear')
			print """q or quit     -> quits application
s or summary   -> Gives summary of your recent reading/saving
sc or scrape   -> Check to see if your favorite sites have put out any new Content
f or favorites -> Update your "favorite" sites
vf or view     -> List favorite sites
c or clean     -> Remove articles added before a certain date, or a certain amount of time ago
st or stats    -> Generate simple statistical summary of reading habits
j or journal   -> Give "reading journal" of past week (IN PROGRESS)
r or roll      -> Pulls a single random articles from many possible sources (IN PROGRESS)
g or guess     -> Scan headlines from news api and find ones that may potentially be of interest (IN PROGRESS)
			"""
		elif next == "s" or next == "summary":
			os.system('clear')
			ReadingSummary(poc)
		elif next == "f" or next == "favorites":
			os.system('clear')
			AddFavorites()
		elif next == "sc" or next == "scrape":
			os.system('clear')
			UpdateArticles(poc)
		elif next == "vf" or next == "view":
			os.system('clear')
			ViewFavorites()
		elif next == "c" or next == "clean":
			os.system('clear')
			CleanUp(poc)
		elif next == "st" or next == "stats":
			os.system('clear')
			ReadingStats(poc)
		elif next == "r" or next == "roll":
			os.system('clear')
			RandomArticle(poc, agg)
		else:
			print "Unknown or unsupported command"

