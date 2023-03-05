import json
from datetime import datetime


class Message:
    def __init__(self, message_file=None, message_text=None):
        self.device = None
        self.text = ""
        self.timestamp = None
        self.channel = None
        if message_file:
            self.get_message_from_file_system(message_file)
        elif message_text:
            self.get_message_from_text(message_text)

    def __str__(self):
        return json.dumps({"Device": self.device, "Text": self.text, "Timestamp": self.timestamp})

    def get_message_from_file_system(self, message_file):
        try:
            with open(message_file, 'r') as f:
                new_message = json.load(f)
            self.device = new_message.get("device", None)
            self.text = new_message.get("message", "")
            self.timestamp = new_message.get("timestamp", None)
            self.channel = new_message.get("channel", None)
            if not all(val is not None for val in [self.device, self.timestamp]):
                raise ValueError("Missing attributes in message file")
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: {message_file} does not exist.")
        except json.decoder.JSONDecodeError:
            raise ValueError(f"Error: {message_file} is not a valid JSON file.")
        except ValueError as e:
            raise ValueError(f"Error: {e}")
        except Exception as e:
            raise Exception(f"Error: Could not load {message_file}: {e}.")

    def get_message_from_text(self, message_text):
        try:
            now = datetime.now()
            timestamp = now.strftime('"timestamp":"%B %d, %Y at %I:%M%p"')
            self.device = "computer"
            self.text = message_text
            self.timestamp = timestamp
            if not all(val is not None for val in [self.device, self.timestamp]):
                raise ValueError("Missing attributes in message object")
        except ValueError as e:
            raise ValueError(f"Error: {e}")
        except Exception as e:
            raise Exception(f"Error: Could not load message object: {e}.")
