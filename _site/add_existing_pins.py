from slackclient import SlackClient
import pinbot

token = open("slack_token.dat", "r").read()
sc = SlackClient(token)

if sc.rtm_connect():
	channels = sc.api_call("channels.list")["channels"]
	for channel in channels:
		print "Now looking at %s" % channel["id"]
		pinned_items = sc.api_call("pins.list", channel=channel["id"])["items"]
		#print pinned_items[::-1]
		#print "\n"
		for item in pinned_items[::-1]:

			if item["type"] == "message": print item["message"]["text"]
			else: print "Pinned item is not a message, so skipping"
			print
			pinbot.add_pin_to_file(item, True)
else:
	print "Connection failed :("