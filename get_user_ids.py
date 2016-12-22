from slackclient import SlackClient
token = open("slack_token.dat", "r").read()
sc = SlackClient(token)

if sc.rtm_connect():
	result = sc.api_call("users.list")
	for member in result["members"]:
		print member["name"] + ": " + member["id"]