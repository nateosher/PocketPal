import requests
import json

def PocketInitialize():
	# Sets up POST request to get verification token
	print "No account detected."
	key = raw_input("Please enter your product key: ")
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
	authorize_res = requests.post(authorize_url, headers=headers, json=authorize_data)
	authorize_res = json.loads(str(authorize_res.text))
	code = authorize_res["code"]

	# Link for user to follow to confirm access
	confirm = "https://getpocket.com/auth/authorize?request_token=%s&redirect_uri=https://www.google.com" % code
	print "Please go to the following url and click confirm:"
	print ""
	print confirm
	print ""
	raw_input("Press Enter when you've done this")
	raw_input("You're sure? (Enter to continue)")

	# Now we get the user's access token and write it to secret.py along with
	# their consumer key

	token_url = "https://getpocket.com/v3/oauth/authorize"
	token_data = {
		"consumer_key" : key,
		"code" : code
	}

	# Take note of the access token, and write it to file with consumer key
	token_res = requests.post(token_url, headers=headers, json=token_data)
	token_res = json.loads(str(token_res.text))
	access_token = token_res["access_token"]

	f = open('data/secret.py', 'w')
	to_write = 'consumer_key = "%s" \naccess_token = "%s"' % (key, access_token)
	f.write(to_write)
	f.close()

	print "Should be working now- thanks for waiting!"

	return 0