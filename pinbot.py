from slackclient import SlackClient
from datetime import datetime
import time
import os.path


token = open("slack_token.dat", "r").read()
print token
sc = SlackClient(token)

def create_empty_page(channel_id):
	channel_name = sc.api_call("channels.info", channel=channel_id)["channel"]["name"]
	page_content = """
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
</html>""" % (channel_name, channel_name)
	with open(channel_id + ".html", 'w') as f:
		f.write(page_content)


def generate_html_item(item):
	channel_id = item["channel_id"]
	channel_name = sc.api_call("channels.info", channel=channel_id)["channel"]["name"]

	pinning_user_id = item["user"]
	pinning_user_name = sc.api_call("users.info", user=pinning_user_id)["user"]["profile"]["real_name"]

	author_user_id = item["item"]["message"]["user"]
	author_user_name = sc.api_call("users.info", user=author_user_id)["user"]["profile"]["real_name"]

	message_text = item["item"]["message"]["text"]

	unix_ts = item["item"]["message"]["ts"]
	#strip everything after the dot
	for i in range(len(unix_ts)):
		if (unix_ts[i] == "."):
			unix_ts = unix_ts[:i]
			break

	timestamp = datetime.fromtimestamp(int(unix_ts)).strftime('%m/%d/%Y %I:%M %p')

	permalink = item["item"]["message"]["permalink"]

	entry = """
		<!--BEGINNING of message pinned by %s -->
		<div class="message">
			<div class="left">
				<div class="profile_wrapper">
					<img class="profile_pic" src="profile_pics/%s.jpg">
					<div class="below_profile_spacer"></div>
				</div>
			</div>
			<div class="right">
				<div class="pinned_by">
					Pinned by %s
				</div>
				<div class="name_time">
					<name>%s</name>
					<a class="permalink" href="%s">
						<time>%s</time>
					</a>
				</div>
				<div class="message_body">
					%s
				</div>
			</div>
		</div>
		<!--END of message pinned by %s -->\n\n
	""" % (pinning_user_name, author_user_id, pinning_user_name, author_user_name,
		   permalink, timestamp, message_text, pinning_user_name)

	return entry

def add_pin_to_file(item):
	channel_id = item["channel_id"]
	file_path = channel_id + ".html"

	#create the file if it doesn't already exist
	if not os.path.isfile(file_path):
		create_empty_page(channel_id)


	new_file = ""
	with open(file_path, 'rw') as f:
		lines = f.readlines()
		counter = 0
		while lines[0] != "		<!-- New messages below this line -->\n" and counter < len(lines):
			new_file += lines[counter]
			lines.remove(lines[0])
		new_file += lines[counter]

		new_file += generate_html_item(item)

		while len(lines) > 0:
			new_file += lines[0]
			lines.remove(lines[0])
	return new_file



def generate_slack_message(item):
	channel_id = item["channel_id"]
	channel_name = sc.api_call("channels.info", channel=channel_id)["channel"]["name"]

	pinning_user_id = item["user"]
	pinning_user_name = sc.api_call("users.info", user=pinning_user_id)["user"]["profile"]["real_name"]

	author_user_id = item["item"]["message"]["user"]
	author_user_name = sc.api_call("users.info", user=author_user_id)["user"]["profile"]["real_name"]

	permalink = item["item"]["message"]["permalink"]

	pin_archive_url = "http://pins.ev3.pw/%s.html" % channel_id

	message = "%s pinned &lt;%s|%s's message&gt;. View a list of all pinned mesages in %s at %s." % (pinning_user_name, permalink, author_user_name, channel_name, pin_archive_url)

	return message

if sc.rtm_connect():
	print "connected"
	while True:
		result = sc.rtm_read()
		for item in result:
			if item["type"] == "pin_added":
				print generate_slack_message(item)
				print item["item"]["message"]["text"]
				print add_pin_to_file(item)
				#print item
else:
	print "connection failed"