import re
import base64
import json
from urllib.parse import parse_qs
from datetime import datetime


class Hermes:
    def __init__(self, config):
        print("Hermes.__init__")
        self.text = None
        self.match = None
        self.file_name = None
        self.message_object = None
        self.prefixes = config['prefixes']
        self.device_types = config['device_types']

    def get_data_from_slack_event(self, event):
        print("Hermes.get_data_from_slack_event")
        event_body = json.loads(event['body'])
        self.text = event_body['event']['blocks'][0]['elements'][0]['elements'][1]['text'].strip()
        message = f'Received @ event: {self.text}'
        target_channel = event_body['event']['channel']
        return message, target_channel

    def get_data_from_slack_command(self,event):
        print("Hermes.get_data_from_slack_command")
        body = base64.b64decode(event['body']).decode('utf-8')
        parsed_body = parse_qs(body)
        self.text = parsed_body['text'][0]
        message = f'Received / command: {self.text}'
        target_channel = parsed_body['channel_id']
        return message, target_channel

    def is_pattern_valid(self):
        print("Hermes.is_pattern_valid")
        for prefix in self.prefixes:
            if self.text.lower().startswith(prefix):
                self.text = re.sub(f'^{prefix}\s*', '', self.text, flags=re.IGNORECASE)
                break
        self.match = re.match(rf'({"|".join(self.device_types)})\s*(\d+)\s*(.*)', self.text, re.IGNORECASE)
        if self.match:
            return True
        else:
            return False

    def get_message_object(self, channel):
        print("Hermes.get_message_object")
        device = f'{self.match.group(1)}{self.match.group(2)}'
        message = self.match.group(3)
        timestamp = datetime.now().strftime('%B %d, %Y at %I:%M%p')
        self.file_name = f'{device}.txt'
        self.message_object = {
            'device': device,
            'message': message,
            'timestamp': timestamp,
            'channel': channel
        }
