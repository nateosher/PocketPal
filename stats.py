# stats.py 
# for storing methods relating to collecting stats on reading habits

def ReadingStats(poc):
	sites = {}
	words = []
	try:
		archived = poc.get_archived()
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

if __name__ == '__main__':
	import secret
	from Pocket import Pocket
	poc = Pocket(secret.consumer_key, secret.access_token)

	ReadingStats(poc)