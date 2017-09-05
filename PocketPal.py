# PocketPal.py
# Given a Pocket object, allows for monitoring and updating
import datetime
import feedparser
from os import system
from random import randint
import json
import requests
from datetime import datetime
from sets import Set

from Pocket import Pocket
from NewsAPI import Aggregator

class PocketPal:
	def __init__(self, pocket=None, agg=None):
		self._pocket = pocket
		self._aggregator = agg
		self._urls = {}
		self._lastChecked = None

	##########################
	###### INITIALIZING ######
	##########################

	def InitializePocket(self):
		# Sets up POST request to get verification token
		print ("Hi! It looks like it's your first time using this app, "
			"so I'm going to walk you through setup.")
		print ""
		print ("In order to use Pocket's API, you need a consumer key. "
		"Rather than have one central one and deal with potential abuses "
		"in my electronic name, I've decided to ask that you register for " 
		"your own. If you'd like to start, log into your pocket account " 
		"and go to \n\n"
		"https://getpocket.com/developer/\n\n"
		"and click \"Create New App.\" (Enter to Continue)")
		raw_input()
		print ("You should now be at a screen titled \"Create an "
		"Application.\" Name your application whatever you want, and provide "
		"a description if you'd like. For platforms, select either windows, "
		"mac, or other (it doesn't really matter, as you'll see in a moment). "
		"Finally, accept the terms of service. (Enter to Continue)")
		raw_input()
		print ("Still with me? Good! You're almost done. Pick a desktop "
		"consumer key from all of the ones offered (for either mac, windows, "
		"or other)\n")
		key = raw_input("Consumer key:\n>> ")
		print ""
		print "One second..."
		print ""
		headers = {
	    	'Content-Type': 'application/json; charset=UTF-8',
	    	'X-Accept': 'application/json',
		}
		authorize_url = "https://getpocket.com/v3/oauth/request"
		key = str(key)
		authorize_data = {
			"consumer_key" : key,
			'redirect_uri' : "http://www.google.com"
		}

		# Actual post request to pocket's API
		try:
			authorize_res = requests.post(authorize_url, headers=headers, 
				json=authorize_data)
		except:
			print "\033[1mError\033[0m- check internet connection and try again"
			return 0
		authorize_res = json.loads(str(authorize_res.text))
		code = authorize_res["code"]

		# Link for user to follow to confirm access
		confirm = ("https://getpocket.com/auth/authorize?"
			"request_token=%s&redirect_uri=https://www.google.com" % code)
		print "Please go to the following url and click confirm:"
		print ""
		print confirm
		print ""
		raw_input("Press Enter when you've done this (after you're redirected"
			" to google)")
		raw_input("You're sure? (Enter to continue)")

		# Now we get the user's access token and write it to secret.py along with
		# their consumer key

		token_url = "https://getpocket.com/v3/oauth/authorize"
		token_data = {
			"consumer_key" : key,
			"code" : code
		}

		# Take note of the access token, and write it to file with consumer key
		try:
			token_res = requests.post(token_url, headers=headers, json=token_data)
		except:
			print "\033[1mError\033[0m- check internet connection and try again"
			return 0
		token_res = json.loads(str(token_res.text))
		access_token = token_res["access_token"]

		self._pocket = Pocket(key, access_token)

		print "Should be working now- thanks for waiting!"

		return 0

	def PocketInitialized(self):
		return self._pocket

	##########################
	###### FEED METHODS ######
	##########################

	def AddFavorites(self):
		print "Enter urls to RSS feeds you want to follow (q or enter to quit)"
		newurls = []
		newurlnames = []
		while True:
			newurl = raw_input("Enter a feed (enter to continue)\n>> ")
			if newurl == "q" or newurl == "":
				break
			elif newurl in self._urls:
				print "You are already tracking this feed"
			else:
				newurls.append(newurl)
				print ("What would you like to nickname this feed?"
					" (q to cancel)")
				while True:
					newname = raw_input(">> ")
					if newname == "q":
						newurls.pop()
					elif newname == "":
						print "Please enter a nonempty nickname"
					else:
						newurlnames.append(newname)
						break
		for i in range(0,len(newurls)):
			self._urls[newurlnames[i]] = newurls[i]
		count = len(self._urls.keys())
		print ("Now following " + str(count) + 
			" feeds (" + str(len(newurls)) + " new)")
		return 0

	def UpdateArticles(self):
		try:
			archived = self._pocket.get_archived()
		except:
			print "\033[1mError\033[0m- check internet connection and try again"
			return 0
		try:
			saved = self._pocket.get_saved()
		except:
			print "\033[1mError\033[0m- check internet connection and try again"
			return 0
		# Title lists
		archivedResolvedTitles = Set([archived[key]["resolved_title"] 
									for key in list(archived.keys())])
		savedResolvedTitles = Set([saved[key]["resolved_title"] 
								for key in list(saved.keys())])
		archivedGivenTitles = Set([archived[key]["given_title"] 
								for key in list(archived.keys())])
		savedGivenTitles = Set([saved[key]["given_title"]
								for key in list(saved.keys())])

		allTitles = (archivedResolvedTitles | savedResolvedTitles |
					archivedGivenTitles | savedGivenTitles)

		startTotal = len(list(saved.keys()))
		done = False
		count = 0
		totalCount = 0
		for name, url in self._urls.iteritems():
			while True:
				n = raw_input(("At most how many articles would you like to "
					"pull from " + name + "? (a for all, f to finish)\n>> "))
				if n == "f":
					done = True
					break
				elif n == "a":
					n = -1
				try:
					n = int(n)
					break
				except ValueError:
					print "Please enter an integer value"

			if done:
				break
			if n != 0:
				print "Pulling down " + url + "..."
				articles = feedparser.parse(url)
			if n == -1:
				n = len(articles["items"])
			count = 0
			for i in range(0,n):
				art = articles["items"][i]
				# FIX THIS
				if art["title"] not in allTitles:
					try:
						self._pocket.add(art["title"], art["link"])
						count += 1
					except:
						print ("\033[1mError\033[0m- check internet"
							" connection and try again")
						return 0
			print "Added " + str(count) + " from " + url
			totalCount += count
			print ""

		print "Added " + str(totalCount) + " new articles"
		return 0

	def ViewFavorites(self):
		feeds = self._urls.keys()
		for feed in feeds:
			print feed + " : " + self._urls[feed]
		return 0

	##########################
	#### NEWS API METHODS ####
	##########################

	def SetAgg(self, agg):
		self._aggregator = agg
		return 0

	def AggEnabled(self):
		return self._aggregator

	def RandomArticle(self):
		valid_categories = ["business", "entertainment", "gaming", "general",
		"music", "politics", "science-and-nature", "sport", "technology"]
		source_hash = {
			"abc-news-au" : "ABC News (AU)",
			"al-jazeera-english" : "Al Jazeera English",
			"ars-technica" : "Ars Technica",
			"associated-press" : "Associated Press",
			"bbc-news" : "BBC News",
			"bbc-sport" : "BBC Sport",
			"bild" : "Bild",
			"bloomberg" : "Bloomberg",
			"breitbart-news" : "Breitbart News",
			"business-insider" : "Business Insider",
			"business-insider-uk" : "Business Insider (UK)",
			"buzzfeed" : "Buzzfeed",
			"cnbc" : "CNBC",
			"cnn" : "CNN",
			"daily-mail" : "Daily Mail",
			"der-tagesspiegel" : "Der Tagesspiegel",
			"die-zeit" : "Die Zeit",
			"engadget" : "Engadget",
			"entertainment-weekly" : "Entertainment Weekly",
			"espn" : "ESPN",
			"espn-cric-info" : "ESPN Cric Info",
			"financial-times" : "Financial Times",
			"focus" : "Focus",
			"football-italia" : "Football Italia",
			"fortune" : "Fortune",
			"four-four-two" : "FourFourTwo",
			"fox-sports" : "Fox Sports",
			"google-news" : "Google News",
			"gruenderszene" : "Gruenderszene",
			"hacker-news" : "Hacker News",
			"handelsblatt" : "Handelsblatt",
			"ign" : "IGN",
			"independent" : "Independent",
			"mashable" : "Mashable",
			"metro" : "Metro",
			"mirror" : "Mirror",
			"mtv-news" : "MTV News",
			"mtv-news-uk" : "MTV News (UK)",
			"national-geographic" : "National Geographic",
			"new-scientist" : "New Scientist",
			"newsweek" : "Newsweek",
			"new-york-magazine" : "New York Magazine",
			"nfl-news" : "NFL News",
			"polygon" : "Polygon",
			"recode" : "Recode",
			"reddit-r-all" : "Reddit /r/all",
			"reuters" : "Reuters",
			"spiegel-online" : "Spiegel Online",
			"t3n" : "T3n",
			"talksport" : "TalkSport",
			"techcrunch" : "Techcrunch",
			"techradar" : "TechRadar",
			"the-economist" : "The Economist",
			"the-guardian-au" : "The Guardian (AU)",
			"the-guardian-uk" : "The Guardian (UK)",
			"the-hindu" : "The Hindu",
			"the-huffington-post" : "The Huffington Post",
			"the-lad-bible" : "The Lad Bible",
			"the-new-york-times" : "The New York Times",
			"the-next-web" : "The Next Web",
			"the-sport-bible" : "The Sport Bible",
			"the-telegraph" : "The Telegraph",
			"the-times-of-india" : "The Times of India",
			"the-verge" : "The Verge",
			"the-wall-street-journal" : "The Wall Street Journal",
			"the-washington-post" : "The Washington Post",
			"time" : "Time",
			"usa-today" : "USA Today",
			"wired-de" : "Wired.de",
			"wirtschafts-woche" : "Wirtschafts Woche"
		}
		# Ask if they want to specify a category
		while True:
			specify = raw_input(("Would you like to specify a category?"
				" (y/n/c):\n>> "))
			if specify == "y":
				while True:
					category = raw_input(("What category would you like?"
						"\nOptions: business, entertainment, gaming, general,"
						" music, science-and-nature, sport, "
						"or technology:\n>> "))
					if category in valid_categories:
						break
					else:
						"Category not recognized- please select a valid category"
				try:
					sources = self._aggregator.get_sources(category)
					break
				except:
					print ("\033[1mError\033[0m- check internet "
						"connection and try again")
					return 0
			elif specify == "n":
				try: 
					sources = self._aggregator.get_sources()
					break
				except:
					print ("\033[1mError\033[0m- check internet "
						"connection and try again")
					return 0
			elif specify == "c":
				return 0
			else:
				print ('Unrecognized command please enter "y," "n," or "c"'
					' for "yes," "no," or "cancel"')

		# Pick source randomly, and display articles
		used_sources = []

		while True:
			system('clear')
			print "Choosing source..."
			source = randint(0, len(sources)-1)
			while source in used_sources and len(used_sources) < len(sources):
				source = (source + 1) % len(sources)

			used_sources.append(source)
			print "Pulling down articles..."
			try:
				articles = self._aggregator.get_arts(sources[source])
				if articles["status"] == "error":
					articles = self._aggregator.get_arts(sources[source], "latest")
				if articles["status"] == "error":
					articles = self._aggregator.get_arts(sources[source], "popular")
				if articles["status"] == "error":
					print "Something went wrong-skipping to next source..."
					continue
			except:
				print ("\033[1mError\033[0m- check internet "
					"connection and try again")
				return 0
			article_list = articles["articles"]
			source_done = False
			used_arts = []
			system('clear')
			print "========================="
			print '\033[4m' + source_hash[sources[source]] + '\033[0m'
			print "========================="
			while not source_done:
				cur_article = randint(0, len(article_list)-1)
				while (cur_article in used_arts 
				and len(used_arts) < len(article_list)):
					cur_article = (cur_article + 1) % len(article_list)
				used_arts.append(cur_article)
				print ""
				print '\033[1m' + article_list[cur_article]["title"] + '\033[0m'
				print "Excerpt: " + article_list[cur_article]["description"]
				while True:
					add = raw_input(("Would you like to add to Pocket? "
						"(y/n/s/c):\n>> "))
					if add == "y":
						self._pocket.add(article_list[cur_article]["title"], 
							article_list[cur_article]["url"])
						print "Article saved!"
						return 0
					elif add == "n":
						break
					elif add == "s":
						source_done = True
						break
					elif add == "c":
						print "Canceled"
						return 0
					else:
						print "Command not recognized"
				if len(used_arts) == len(article_list):
					break

	def EnableAgg(self):
		print ("Would you like to enable PocketPal to connect"
			" to https://newsapi.org/? This will allow PocketPal to suggest"
			" random articles from a broad range of sources. However,"
			" you will have to register (for free!) for an api"
			" key (y/n):")
		while True:
			enable = raw_input(">> ")
			if enable == "n":
				return 0
			elif enable == "y":
				print ("Great! Please visit https://newsapi.org/register"
					" to get your api key")
				print "When you have it, enter it here (q to cancel):"
				while True:
					api_key = raw_input(">> ")
					if api_key == "q":
						return 0
					else:
						print "Just one second please"
						test_agg = Aggregator(api_key)
						print "Connecting to server..."
						try:
							sources = test_agg.get_sources()
						except:
							print ("\033[1mError\033[0m- check internet "
								"connection and try again")
							return 0
						print "Testing api key..."
						source = randint(0,len(sources) - 1)
						try:
							res = test_agg.get_arts(sources[source])
						except:
							print ("\033[1mError\033[0m- check internet "
								"connection and try again")
							return 0
						if (res['status'] == 'ok' 
							or res['code'] != 'apiKeyInvalid'):
							print "Success!"
							print "Saving key..."
							self._aggregator = test_agg
							return 0
						else:
							print ("Error: invalid api key- please re-enter your"
								" api key (q to cancel):")

			else:
				print "Didn't quite catch that"

	##########################
	##### STATSY METHODS #####
	##########################

	def ReadingStats(self):
		sites = {}
		words = []
		try:
			archived = self._pocket.get_archived()
		except:
			print "\033[1mError\033[0m- check internet connection and try again"
			return 0
		nread = len(archived.keys())
		maxWords = -1
		maxKey = None
		for key in archived.keys():
			cur = archived[key]
			words.append(int(cur["word_count"]))
			if int(cur["word_count"]) > maxWords:
				maxWords = int(cur["word_count"])
				maxKey = key
			urlStem = cur["resolved_url"].split("/")[2]
			urlStem = urlStem.split(".")
			if len(urlStem) == 2:
				urlStem = urlStem[0]
			else:
				urlStem = urlStem[1]

			if urlStem in sites:
				sites[urlStem] += 1
			else:
				sites[urlStem] = 1

		print "Total # of articles read in Pocket: " + str(nread)
		print ""

		# Get top 5 sites
		top5 = sorted(sites, key=sites.get, reverse=True)[:5]
		print "Top 5 news sources:"
		t5Count = 0
		for key in top5:
			t5Count += sites[key]
			print key + ": " + str(sites[key])

		print ""

		print ("You get " + str((float(t5Count)/nread)*100)[0:2] +
			" percent of your reading from these sources")

		print ""

		print "Average # of words per article: " + str(sum(words)/len(words))
		print "Total # of words read in Pocket career: " + str(sum(words))
		print ('Longest article: "' + 
			archived[maxKey]["resolved_title"] + '" at ' + 
			str(maxWords) + ' words')
		print ""
		return 0

	##########################
	###### MISC METHODS ######
	##########################

	def CalculateChange(self, oldDate, newDate):
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
					return (prefix + str(newDate[i] - oldDate[i]) + 
							" " + date_hash[i] + "s")

	def RecentReading(self):
		# Get current date as list of ints
		current_date = list(datetime.now().timetuple()[0:6])
		# Make request to see how many articles user has
		try:
			results = self._pocket.get_saved()
		except:
			print "\033[1mError\033[0m- check internet connection and try again"
			return 0
		try:
			readArts = self._pocket.get_archived()
		except:
			print "\033[1mError\033[0m- check internet connection and try again"
			return 0

		# Get number of saved articles
		counter = len(list(results.keys()))
		numRead = len(list(readArts.keys()))

		current_date.append(counter)
		current_date.append(numRead)

		print "You have " + str(counter) + " saved articles"
		print "You have read " + str(numRead) + " articles"
		if self._lastChecked:
			print self.CalculateChange(self._lastChecked, current_date)
		self._lastChecked = current_date
		return 0

	def CleanUp(self):
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
				print ("Format error- be sure to pad month and"
					" day with 0's if necessary")
				print "Enter empty string to cancel action"
		print "Retrieving saved articles..."
		try:
			saved = self._pocket.get_saved()
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
							self._pocket.delete(curID)
							print "Article deleted"
							break
						except:
							print ("\033[1mError\033[0m- check internet "
								"connection and try again")
							return 0
					elif resp == "a":
						try:
							self._pocket.archive(curID)
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

###############################################################################

def main():
	import pickle
	import os
	import data.secret as secret
	from Pocket import Pocket
	from NewsAPI import Aggregator
	import pprint

	if not os.path.isfile('pocketpal.pkl'):
		pp = PocketPal(poc)
		pp.AddFavorites()
		with open('pocketpal.pkl', 'wb') as outfile:
			pickle.dump(pp, outfile, -1)
	else:
		p_file = open('pocketpal.pkl', 'rb')
		pp = pickle.load(p_file)
		p_file.close()


if __name__ == '__main__':
	main()

