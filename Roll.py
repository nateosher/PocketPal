# Roll.py
# Providing a method to pull a random article

from random import randint
from os import system

def RandomArticle(poc, agg):
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
	while True:
		specify = raw_input(("Would you like to specify a category?"
			" (y/n/c):\n>> "))
		if specify == "y":
			while True:
				category = raw_input(("What category would you like?"
					"\nOptions: business, entertainment, gaming, general,"
					" music, politics, science-and-nature, sport, "
					"or technology:\n>> "))
				if category in valid_categories:
					break
				else:
					"Category not recognized- please select a valid category"
			sources = agg.get_sources(category)
			break
		elif specify == "n":
			sources = agg.get_sources()
			break
		elif specify == "c":
			return 0
		else:
			print ('Unrecognized command please enter "y," "n," or "c"'
				' for "yes," "no," or "cancel"')

	used_sources = []

	while True:
		system('clear')
		print "Choosing source..."
		source = randint(0, len(sources)-1)
		while source in used_sources and len(used_sources) < len(sources):
			source = (source + 1) % len(sources)
		used_sources.append(source)
		print "Pulling down articles..."
		articles = agg.get_arts(sources[source])
		if articles["status"] == "error":
			articles = agg.get_arts(sources[source], "latest")
		if articles["status"] == "error":
			articles = agg.get_arts(sources[source], "popular")
		if articles["status"] == "error":
			print "Something went wrong"
			continue
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
					poc.add(article_list[cur_article]["title"], 
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






















