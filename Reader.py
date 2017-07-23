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

# TODO: Delete functionality with regex?

# TODO: Only add articles published after a certain date
# Checks rss feeds of favorite feeds and attempts to add all of them
# to pocket. 
# @param poc: Pocket object. 
def UpdateArticles(poc):
	urls = []
	f = open("feeds.txt", "r")
	count = 0
	for line in f:
		url = line.rstrip()
		print "Pulling down " + url + "..."
		articles = feedparser.parse(url)
		for art in articles["items"]:
			archived = poc.get_archived()
			poc.add(art["title"], art["link"])
			count += 1
	print "Added " + str(count) + " articles"
	return 0








if __name__ == '__main__':
	from Pocket import Pocket
	import secret
	poc = Pocket(secret.consumer_key, secret.access_token)
	UpdateArticles(poc)





