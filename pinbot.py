from slackclient import SlackClient
from datetime import datetime
import time


token = open("slack_token.dat", "r").read()
#token = "xoxb-110109408469-2NStnpT0jxgbNS9A4Cs5izeO"
print token
sc = SlackClient(token)

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


def generate_slack_message(item):
	channel_id = item["channel_id"]
	channel_name = sc.api_call("channels.info", channel=channel_id)["channel"]["name"]

	pinning_user_id = item["user"]
	pinning_user_name = sc.api_call("users.info", user=pinning_user_id)["user"]["profile"]["real_name"]

	author_user_id = item["item"]["message"]["user"]
	author_user_name = sc.api_call("users.info", user=author_user_id)["user"]["profile"]["real_name"]

	message_text = item["item"]["message"]["text"]

	message = ""
	message += pinning_user_name
	message += " pinned "
	message += author_user_name
	message += "'s message in #"
	message += channel_name
	message += ".\nView an archive of all pinned messages at "
	message += ""#some url
	message += "."
	return message

if sc.rtm_connect():
	print "connected"
	while True:
		result = sc.rtm_read()
		for item in result:
			if item["type"] == "pin_added":
				print generate_slack_message(item)
				print item["item"]["message"]["text"]
				print generate_html_item(item)
				#print item
else:
	print "connection failed"