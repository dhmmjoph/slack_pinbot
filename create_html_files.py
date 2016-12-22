from slackclient import SlackClient
import os.path
from pinbot import create_empty_page

token = open("slack_token.dat", "r").read()
sc = SlackClient(token)

if sc.rtm_connect():
	result = sc.api_call("channels.list")
	for channel in result["channels"]:
		print channel["name"] + ": " + channel["id"]
		if not os.path.isfile(channel["id"] + ".html"):
			create_empty_page(channel["id"])
