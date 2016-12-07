from slackclient import SlackClient
token = open("slack_token.dat", "r").read()
sc = SlackClient(token)

if sc.rtm_connect():
	result = sc.api_call("channels.list")
	for channel in result["channels"]:
		print "Here are some channels"
		print channel["name"] + ": " + channel["id"]