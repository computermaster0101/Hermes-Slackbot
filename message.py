import json
from datetime import datetime

class Message:
    def __init__(self, message_file=None, message_object=None):
        self.device = None
        self.text = ""
        self.timestamp = None
        if message_file:
            try:
                with open(message_file, 'r') as f:
                    new_message = json.load(f)
                self.device = new_message.get("device", None)
                self.text = new_message.get("message", "")
                self.timestamp = new_message.get("timestamp", None)
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
        elif message_object:
            try:
                self.device = message_object.get("device", None)
                self.text = message_object.get("message", "")
                self.timestamp = message_object.get("timestamp", None)
                if not all(val is not None for val in [self.device, self.timestamp]):
                    raise ValueError("Missing attributes in message object")
            except ValueError as e:
                raise ValueError(f"Error: {e}")
            except Exception as e:
                raise Exception(f"Error: Could not load message object: {e}.")
