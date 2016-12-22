from slackclient import SlackClient
import pinbot

token = open("slack_token.dat", "r").read()
sc = SlackClient(token)


def main():
	if sc.rtm_connect():
		print "connected"
		while True:
			result = sc.rtm_read()
			for item in result:
				if item["type"] == "pin_added":
					print pinbot.generate_slack_message(item)
					print item["item"]["message"]["text"]
					pinbot.add_pin_to_file(item)
					pinbot.push_changes(item)
					pinbot.send_message(item)
					#pinbot.delete_pins_if_necessary(item)
	else:
		print "connection failed"


if __name__ == '__main__':
	main()