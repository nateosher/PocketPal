# Reader.py
# For methods relating to rss shenanigans
# https://wiki.python.org/moin/RssLibraries
import datetime
import feedparser

# Add favorite rss feeds
def AddFavorites():
	print "Enter urls to RSS feeds you want to follow"
	f = open("data/feeds.txt", "r")
	oldurls = []
	for line in f:
		oldurls.append(line.rstrip())
	f.close()
	newurls = []
	while True:
		newurl = raw_input()
		if newurl == "":
			break
		elif newurl in oldurls:
			print "You are already tracking this feed"
		else:
			newurls.append(newurl)
	f = open("data/feeds.txt", 'a')
	for url in newurls:
		f.write(url + "\n")
	f.close()
	count = 0
	f = open("data/feeds.txt", "r")
	for line in f:
		count += 1
	print "Now following " + str(count) + " feeds (" + str(len(newurls)) + " new)"
	return 0
	
# Checks rss feeds of favorite feeds and attempts to add all of them
# to pocket. 
# @param poc: Pocket object. 
def UpdateArticles(poc):
	urls = {}
	f = open("data/feeds.txt", "r")
	count = 0
	archived = poc.get_archived()
	saved = poc.get_saved()
	read_titles = [archived[key]["resolved_title"] for key in list(archived.keys())]
	saved_titles = [saved[key]["resolved_title"] for key in list(saved.keys())]
	startTotal = len(list(saved.keys()))
	for line in f:
		line_list = line.split(">>>")
		urls[line_list[1].rstrip()] = line_list[0]

	done = False
	for name, url in urls.iteritems():
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
			if (art["title"] not in read_titles and 
				art["title"] not in saved_titles):
				poc.add(art["title"], art["link"])
				count += 1
		print "Added " + str(count) + " from " + url
		print ""
	endTotal = len(list(poc.get_saved().keys()))

	print "Added " + str(endTotal - startTotal) + " new articles"
	return 0

def ViewFavorites():
	f = open("data/feeds.txt", "r")
	for line in f:
		print line.rstrip()
	return 0






if __name__ == '__main__':
	from Pocket import Pocket
	import secret
	poc = Pocket(secret.consumer_key, secret.access_token)
	UpdateArticles(poc)





