from slackclient import SlackClient
from datetime import datetime
import time
import os.path
import codecs

token = open("slack_token.dat", "r").read()
#print token
sc = SlackClient(token)


def create_empty_page(channel_id):
	channel_name = sc.api_call("channels.info", channel=channel_id)["channel"]["name"]
	page_content = """---
layout: pins
channel: %s
---
""" % channel_name
	with codecs.open(channel_id + ".html", 'w' ,'utf-8') as f:
		f.write(page_content)
	print "Created file for %s" % channel_name

def is_slack_link(word):
	for i in range(len(word)):
		if word[i] == "<":
			for j in range(i, len(word)):
				if word[j] == ">":
					return True
	return False

def html_format(message):
	message_split = message.split()
	new = ""
	for word in message_split:
		if is_slack_link(word):
			lt = word.find("<")
			gt = word.find(">")
			bar = word.find("|")#find() will return -1 if the target is not found
			if bar >= 0:#there is some sort of separate link text
				address = word[lt+1:bar]
				text = word[bar+1:gt]
				if address[0] == "@": #it's a link to a user
					user_name = sc.api_call("users.info", user=address[1:])["user"]["name"]
					address = "https://frendgroop.slack.com/team/%s" % user_name
				elif address[0] == "C": #it's a link to a channel
					channel_name = sc.api_call("channels.info", channel=address)["channel"]["name"]
					address = "https://frendgroop.slack.com/messages/%s" % channel_name
				#if it's a normal link to a URl we don't need to change the address
			else:#it's just a URL, @ mention, or channel name
				if word[lt+1] == "@":#reference to a user
					user_name = sc.api_call("users.info", user=word[lt+2:gt])["user"]["name"]
					address = "https://frendgroop.slack.com/team/%s" % user_name
					text = "@%s" % user_name
				elif word[1] == "C":
					channel_name = sc.api_call("channels.info", channel=word[lt+1:gt])["channel"]["name"]
					address = "https://frendgroop.slack.com/messages/%s" % channel_name
					text = "#%s" % channel_name
				else:
					address = word[lt+1:gt]
					text = word[lt+1:gt]

			new += "%s<a href=\"%s\">%s</a>%s" % (word[:lt], address, text, word[gt+1:])
		else: new += word
		new += " "
	new += " "
	print new
	return new

def generate_html_item(item, existing=False):
	if not existing: channel_id = item["channel_id"]
	else: channel_id = item["channel"]
	channel_name = sc.api_call("channels.info", channel=channel_id)["channel"]["name"]

	if not existing: pinning_user_id = item["user"]
	else: pinning_user_id = item["created_by"]
	pinning_user_name = sc.api_call("users.info", user=pinning_user_id)["user"]["profile"]["real_name"]

	if not existing: author_user_id = item["item"]["message"]["user"]
	else: author_user_id = item["message"]["user"] 
	author_user_name = sc.api_call("users.info", user=author_user_id)["user"]["profile"]["real_name"]

	if not existing: message_text = item["item"]["message"]["text"]
	else: message_text = item["message"]["text"] 
	message_text = html_format(message_text)

	if not existing: unix_ts = item["item"]["message"]["ts"]
	else: unix_ts = item["message"]["ts"]

	#strip everything after the dot
	for i in range(len(unix_ts)):
		if (unix_ts[i] == "."):
			unix_ts = unix_ts[:i]
			break

	timestamp = datetime.fromtimestamp(int(unix_ts)).strftime('%m/%d/%Y %I:%M %p')

	if not existing: permalink = item["item"]["message"]["permalink"]
	else: permalink = item["message"]["permalink"]

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


def add_pin_to_file(item, existing=False):
	if item["type"] != "message": return
	if not existing: channel_id = item["channel_id"]
	else: channel_id = item["channel"]
	file_path = channel_id + ".html"

	#create the file if it doesn't already exist
	if not os.path.isfile(file_path):
		create_empty_page(channel_id)


	new_file = ""
	with codecs.open(file_path, 'r', 'utf-8') as f:
		lines = f.readlines()
		for line in lines[:4]:
			new_file += line
		new_file += generate_html_item(item, existing)
		for line in lines[4:]:
			new_file += line
	with codecs.open(file_path, 'w', 'utf-8') as f:
		f.write(new_file)
		

def push_changes(item):
	channel_id = item["channel_id"]
	channel_name = sc.api_call("channels.info", channel=channel_id)["channel"]["name"]

	pinning_user_id = item["user"]
	pinning_user_name = sc.api_call("users.info", user=pinning_user_id)["user"]["profile"]["real_name"]

	add_command = "git add ."
	commit_message = "add pin by %s in %s (AUTO-COMMIT)" % (pinning_user_name, channel_name)
	commit_command = "git commit -m \"%s\"" % commit_message
	push_command = "git push origin master"

	os.system(add_command)
	os.system(commit_command)
	os.system(push_command)


def generate_slack_message(item):
	channel_id = item["channel_id"]
	channel_name = sc.api_call("channels.info", channel=channel_id)["channel"]["name"]

	pinning_user_id = item["user"]
	pinning_user_name = sc.api_call("users.info", user=pinning_user_id)["user"]["profile"]["real_name"]

	author_user_id = item["item"]["message"]["user"]
	author_user_name = sc.api_call("users.info", user=author_user_id)["user"]["profile"]["real_name"]

	permalink = item["item"]["message"]["permalink"]

	pin_archive_url = "http://pins.ev3.pw/%s.html" % channel_id

	message = "%s pinned <%s|%s's message>. View a list of all pinned mesages in #%s at %s." % (pinning_user_name, permalink, author_user_name, channel_name, pin_archive_url)

	return message

def send_message(item):
	message_text = generate_slack_message(item)
	channel_id = item["channel_id"]
	try:
		sc.api_call("chat.postMessage", channel=channel_id, text=message_text, as_user="true")
	except ValueError:
		print "ValueError: message probably got sent anyway so whatever"