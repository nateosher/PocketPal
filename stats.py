# stats.py 
# for storing methods relating to collecting stats on reading habits

def ReadingStats(poc):
	sites = {}
	words = []
	archived = poc.get_archived()
	for key in archived.keys():
		cur = archived[key]
		words.append(int(cur["word_count"]))
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

	# Get top 5 sites
	top5 = sorted(sites, key=sites.get, reverse=True)[:5]
	print "Top 5 news sources"
	for key in top5:
		print key + " : " + str(sites[key])

	print ""

	print "Average # of words per article: " + str(sum(words)/len(words))
	print ""
	return 0

if __name__ == '__main__':
	import secret
	from Pocket import Pocket
	poc = Pocket(secret.consumer_key, secret.access_token)

	ReadingStats(poc)