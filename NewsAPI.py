# NewsAPI.py
# Houses the Aggregator class, for interfacing with the news NewsAPI

from requests import get
from json import loads

class Aggregator:
	def __init__(self, key):
		self._key = key
		self._baseurl = "https://newsapi.org/v1/"

	# Getter method for key- you will probably never need this, and
	# you definitely won't need a setter method
	def get_key(self):
		return self._key

	# Returns a list of all possible sources from api
	# If no category is specified, defaults to all
	# Valid categories include: business, entertainment, gaming, 
	# general, music, politics, science-and-nature, sport, technology
	def get_sources(self, category=""):
		req_url = "https://newsapi.org/v1/sources?language=en&category=%s" % category
		res = get(req_url)
		raw_source = loads(res.content)["sources"]
		source_list = []
		for source in raw_source:
			source_list.append(source["id"])

		return source_list

	# Get articles from a specified source
	# Articles can be sorted by top, latest, or popular (defaults to top)
	def get_arts(self, source, sortBy="top"):
		req_url = ("https://newsapi.org/v1/articles?source=%s&sortBy=%s"
			"&apiKey=%s") % (source, sortBy, self._key)
		res = get(req_url)
		raw_source = loads(res.content)
		return raw_source




if __name__ == '__main__':
	from data import secret
	agg = Aggregator("66e7db5aff244cf18d4fe854f0d4bc3b")
	# print agg.get_sources("technology")
	# arts = agg.get_arts("the-new-york-times", "top")
	arts = agg.get_arts("the-new-york-times")
	print arts
	print arts["status"] == "error"




