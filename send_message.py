import requests

class MessageSender:
    def __init__(self, slack_webhook_url, matrix_access_token, matrix_room_id, skype_access_token, skype_conversation_id):
        self.slack_webhook_url = slack_webhook_url
        self.matrix_url = "https://matrix.org/_matrix/client/r0"
        self.matrix_access_token = matrix_access_token
        self.matrix_room_id = matrix_room_id
        self.skype_url = "https://smba.trafficmanager.net/apis/v3/conversations"
        self.skype_access_token = skype_access_token
        self.skype_conversation_id = skype_conversation_id

    def slack(self, message):
        data = {"text": message}
        response = requests.post(self.slack_webhook_url, json=data)
        response.raise_for_status()
        return response.text

    def matrix(self, message):
        url = f"{self.matrix_url}/rooms/{self.matrix_room_id}/send/m.room.message"
        headers = {
            "Authorization": f"Bearer {self.matrix_access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "msgtype": "m.text",
            "body": message
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.text

    def skype(self, message):
        url = f"{self.skype_url}/{self.skype_conversation_id}/activities"
        headers = {
            "Authorization": f"Bearer {self.skype_access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "type": "message",
            "text": message
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.text





sender = MessageSender(
    slack_webhook_url="https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXX",
    matrix_access_token="YOUR_MATRIX_ACCESS_TOKEN",
    matrix_room_id="YOUR_MATRIX_ROOM_ID",
    skype_access_token="YOUR_SKYPE_ACCESS_TOKEN",
    skype_conversation_id="YOUR_SKYPE_CONVERSATION_ID"
)

# Send a message to Slack
sender.slack("Hello, Slack!")

# Send a message to Matrix
sender.matrix("Hello, Matrix!")

# Send a message to Skype
sender.skype("Hello, Skype!")
