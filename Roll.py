# Roll.py
# Providing a method to pull a random article

from random import randint

def RandomArticle(poc, agg):
	valid_categories = ["business", "entertainment", "gaming", "general",
	"music", "politics", "science-and-nature", "sport", "technology"]
	select = False
	while True:
		specify = raw_input("Would you like to specify a category? (y/n/c): ")
		if specify == "y":
			select = True
			break
		elif specify == "n":
			break
		elif specify == "c":
			return 0
		else:
			print ('Unrecognized command please enter "y," "n," or "c"'
				' for "yes," "no," or "cancel"')
	if select:
		while True:
			category = raw_input(("What category would you like?"
				"\nOptions: business, entertainment, gaming, general,"
				" music, politics, science-and-nature, sport, or technology: "))
			if category in valid_categories:
				break
			else:
				"Category not recognized- please select a valid category"

	if not select:
		sources = agg.get_sources()
	else:
		sources = agg.get_sources(category)
	used_sources = []

	print sources

	while True:
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
		while not source_done:
			cur_article = randint(0, len(article_list)-1)
			while (cur_article in used_arts 
			and len(used_arts) < len(article_list)):
				cur_article = (cur_article + 1) % len(article_list)
			used_arts.append(cur_article)
			print ""
			print "Here's an article from " + sources[source] + ":"
			print article_list[cur_article]["title"]
			while True:
				add = raw_input("Would you like to add to Pocket? (y/n/s/c): ")
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






















