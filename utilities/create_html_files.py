from slackclient import SlackClient
import os.path
token = open("slack_token.dat", "r").read()
sc = SlackClient(token)

if sc.rtm_connect():
	result = sc.api_call("channels.list")
	for channel in result["channels"]:
		print channel["name"] + ": " + channel["id"]
		if not os.path.isfile(channel["id"] + ".html"):
			with open(channel["id"] + ".html", 'w') as f:
				channel_name = channel["name"]
				empty_file = """
<html>
	<head>
		<title>Frendgroop pinned messages | #%s</title>
		<link rel="stylesheet" type="text/css" href="slack.css">
	</head>
	<body>
		<h1>Pinned messages archive for #%s</h1>
		<h4>Most recently-pinned messages displayed first</h4>

		<!-- New messages below this line -->

	</body>
</html>
""" % (channel_name, channel_name)
				f.write(empty_file)
				print "     created file for %s" % channel_name
				print