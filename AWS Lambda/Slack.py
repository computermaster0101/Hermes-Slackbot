import urllib.parse
import urllib.request


class Slack:

    def __init__(self, config):
        print("Slack.__init__")
        self.url = "https://slack.com/api/chat.postMessage"
        self.token = config['token']
        self.default_channel = config['channel']
        self.target_channel = None
        self.message = [""]

        self.request = urllib.request.Request(self.url, method="POST")
        self.request.add_header("Content-Type", "application/x-www-form-urlencoded")

    def send(self):
        print("Slack.send")
        channel = self.target_channel if self.target_channel else self.default_channel
        output = "\n".join(self.message)

        data = urllib.parse.urlencode(
            (
                ("token", self.token),
                ("channel", channel),
                ("text", output)
            ),
            safe=":"
        )
        data = data.encode("ascii")

        self.request.data = data
        x = urllib.request.urlopen(self.request).read()
        print(f"Slack.send:\n{x}")

    def clear(self):
        print("Slack.clear")
        self.message = [""]
