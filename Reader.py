# Reader.py
# For methods relating to rss shenanigans
# https://wiki.python.org/moin/RssLibraries
import datetime

import feedparser

# Add favorite rss feeds
def AddFavorites():
	# TODO: Check for a feed before adding it
	print "Enter urls to RSS feeds you want to follow"
	urls = []
	while True:
		newurl = raw_input()
		if newurl == "":
			break
		urls.append(newurl)
	f = open("feeds.txt", 'a')
	for url in urls:
		f.write(url + "\n")
	f.close()
	count = 0
	f = open("feeds.txt", "r")
	for line in f:
		count += 1
	print "Now following " + str(count) + " feeds"
	return 0

#TODO: Delete functionality with regex?

def UpdateArticles():
	urls = []
	f = open("feeds.txt", "r")
	for line in f:
		url = line.rstrip()
		print "Pulling down " + url + "..."
		print ""
		articles = feedparser.parse(url)
		for art in articles["items"]:
			print art["title"]
			print art["link"]
			print ""
	return 0








if __name__ == '__main__':
	UpdateArticles()