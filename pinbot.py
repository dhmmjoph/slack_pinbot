from slackclient import SlackClient
import time


token = open("slack_token.dat", "r").read()
sc = SlackClient(token)

def generate_html_item(item):
	channel_id = item["channel_id"]
	channel_name = sc.api_call("channels.info", channel=channel_id)["channel"]["name"]

	pinning_user_id = item["user"]
	pinning_user_name = sc.api_call("users.info", user=user_id)["user"]["profile"]["real_name"]

	message_text = item["item"]["message"]["text"]

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
	message += "."
	return message

if sc.rtm_connect():
	while True:
		result = sc.rtm_read()
		for item in result:
			if item["type"] == "pin_added":
				'''channel_name = sc.api_call("channels.info", channel=item["channel_id"])["channel"]["name"]
				user_name = sc.api_call("users.info", user=item["user"])["user"]["profile"]["real_name"]
				message_text = item["item"]["message"]["text"]
				print "Message pinned in #" + channel_name + " by " + user_name + ":"
				print message_text'''
				print generate_slack_message(item)
				