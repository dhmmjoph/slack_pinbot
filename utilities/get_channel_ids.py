from slackclient import SlackClient
token = open("slack_token.dat", "r").read()
sc = SlackClient(token)

if sc.rtm_connect():
	result = sc.api_call("channels.list")
	for channel in result["channels"]:
		print channel["name"] + ": " + channel["id"]
		with open(channel + ".html", 'r') as f:
			if (f.read = )
