import urllib.parse
import urllib.request
import certifi
import ssl

class MessageSender:

    def __init__(self, slack_token):
        self.slack_url = "https://slack.com/api/chat.postMessage"
        self.slack_token = slack_token

    def slack(self, message, channel):
        data = urllib.parse.urlencode(
            (
                ("token", self.slack_token),
                ("channel", channel),
                ("text", message)
            )
        )
        data = data.encode("ascii")

        context = ssl.create_default_context(cafile=certifi.where())
        request = urllib.request.Request(self.slack_url, data=data, method="POST")
        request.add_header("Content-Type", "application/x-www-form-urlencoded")
        x = urllib.request.urlopen(request).read()
        #print(x)
