from slackclient import SlackClient

token = open("slack_token.dat", "r").read()
sc = SlackClient(token)

if sc.rtm_connect():
	toc = '''---
layout: toc
---
'''
	result = sc.api_call("channels.list")
	for channel in result["channels"]:
		toc += "<p>&bull; <a class=\"channel_link\" href=\"{{ site.url }}/%s.html\">#%s</a></p>\n" % (channel["id"], channel["name"])
	#toc += "</ul>"
	with open("index.html", 'w') as f:
		f.write(toc)

else:
	print "connection failed"