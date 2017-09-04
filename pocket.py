# Pocket.py
# Pocket class, for interfacing with the pocket api

from requests import post
from json import loads

class Pocket:
	def __init__(self, consKey, accToken):
		self._info = {"consumer_key": consKey, "access_token" : accToken}
		self._baseUrl = "https://getpocket.com/v3/"

	# Returns a dictionary of articles, where each article is also a dictionary
	def get_saved(self):
		res = post(self._baseUrl + "get", json = self._info)
		res = loads(str(res.text))
		return res["list"]

	# Returns a dictionary of archived articles, where each article is also
	# a dictionary
	def get_archived(self):
		arch_info = {"state":"archive"}
		arch_info.update(self._info)
		res = post(self._baseUrl + "get", json = arch_info)
		res = loads(str(res.text))
		return res["list"]

	# Add a new article to pocket
	# @param title: String. title of the article
	# @param url  : String. url of article
	# Returns summary of what was sent as dictionary, including response code
	def add(self, title, url):
		add_info = {"title":title, "url":url}
		add_info.update(self._info)
		res = post(self._baseUrl + "add", json = add_info)
		return loads(str(res.text))["item"]

	# Delete article from user's library
	# @param artID: int. articles assigned ID in pocket
	def delete(self, artID):
		del_info = {"actions" : [{"action" : "delete", "item_id" : artID}]}
		del_info.update(self._info)
		res = post(self._baseUrl + "send", json = del_info)
		return res

	# Archive article from user's library
	# @param artID: int. articles assigned ID in pocket
	def archive(self, artID):
		arch_info = {"actions" : [{"action" : "archive", "item_id" : str(artID)}]}
		arch_info.update(self._info)
		res = post(self._baseUrl + "send", json = arch_info)
		return res


def main():
	import secret
	poc = Pocket(secret.consumer_key, secret.access_token)

	# # get_saved() test
	# arts = poc.get_saved()
	# for k1 in list(arts.keys()):
	# 	for k2 in list(arts[k1].keys()):
	# 		print k2, ":", arts[k1][k2]
	# 	print "========"

	# # add_new_article() test
	# title = "Best in Classified"
	# url = ("http://slatestarcodex.com/2017/07/20/
	# classified-thread-2-best-in-classified/")
	# resp = poc.add(title, url)
	# for key in resp.keys():
	# 	print key,":", resp[key]

	# get_archived() test
	archs = poc.get_archived()
	for key in archs.keys():
		print archs[key]["given_title"]
		print archs[key]["resolved_title"]
		print "=========================="

	# # archive() test
	# poc.archive(1827984249)

	# # delete() test
	# res = poc.delete(1827984249)
	# print loads(res.text)["status"]


if __name__ == '__main__':
	main()