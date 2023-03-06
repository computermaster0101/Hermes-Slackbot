import re
import base64
import datetime
import json
from urllib.parse import parse_qs
from datetime import datetime
from upload_file import FileUploader
from send_message import MessageSender


class HermesGatekeeper:
    def __init__(self, config_file):
        self.destination_slack_channel = None
        self.respond = True
        self.response = []
        self.text = None
        self.match = None
        self.file_name = None
        self.message_object = None
        try:
            config = json.load(open(config_file))
            self.tokens = {
                "hermes_relay_key": config["hermes_relay_key"],
                "slack_at_api_key": config["slack_at_api_key"],
                "slack_slash_api_key": config["slack_slash_api_key"],
                "dialogflow_api_key": config["dialogflow_api_key"]
            }
            self.nextcloud_username = config["nextcloud_username"]
            self.nextcloud_access_token = config["nextcloud_access_token"]
            self.nextcloud_url = config["nextcloud_url"]
            self.dropbox_access_token = config["dropbox_access_token"]
            self.slack_token = config["slack_token"]
            self.default_slack_channel = config["default_slack_channel"]

            self.file_uploader = FileUploader(dropbox_access_token=self.dropbox_access_token,
                                              nextcloud_username=self.nextcloud_username,
                                              nextcloud_access_token=self.nextcloud_access_token,
                                              nextcloud_url=self.nextcloud_url)

            self.message_sender = MessageSender(self.slack_token)

        except FileNotFoundError as e:
            print(f"Error loading config from {config_file}: {e}")
        except Exception as e:
            print(f"Error loading config: {e}")

    def is_key_valid(self, api_key):
        if api_key in self.tokens.values():
            return True
        else:
            return False

    def is_pattern_valid(self):
        self.match = re.match(r'system\s*(\d+)\s*(.*)', self.text)
        if self.match:
            return True
        else:
            return False

    def get_data_from_event(self, event):
        apikey = event['queryStringParameters']['apikey']
        if apikey == self.tokens['slack_slash_api_key']:
            body = base64.b64decode(event['body']).decode('utf-8')
            parsed_body = parse_qs(body)
            self.text = parsed_body['text'][0]
            self.destination_slack_channel = None
            self.respond = True
            self.response.append(f'Received / command: {self.text}')
        elif apikey == self.tokens['slack_at_api_key']:
            event_body = json.loads(event['body'])
            self.text = event_body['event']['blocks'][0]['elements'][0]['elements'][1]['text'].strip()
            self.destination_slack_channel = event_body['event']['channel']
            self.respond = True
            self.response.append(f'Received @ command: {self.text}')
        else:
            self.response.append("Not Yet Implemented")

    def get_message_object(self):
        device = f'system{self.match.group(1)}'
        message = self.match.group(2)
        timestamp = datetime.now().strftime('%B %d, %Y at %I:%M%p')
        channel = self.destination_slack_channel
        if channel is None:
            channel = self.default_slack_channel
        self.file_name = f'{device}.txt'
        self.message_object = {
            'device': device,
            'message': message,
            'timestamp': timestamp,
            'channel': channel
        }

    def file_upload(self):
        self.file_uploader.upload(self.file_name, json.dumps(self.message_object))

    def send_message(self):
        output = self.get_output_string()
        print(output)
        if self.respond:
            if self.destination_slack_channel:
                self.message_sender.slack(output, self.destination_slack_channel)
            else:
                self.message_sender.slack(output, self.default_slack_channel)

    def get_output_string(self):
        output = ""
        for line in self.response:
            output = f'{output}\n{line}'
        return output
