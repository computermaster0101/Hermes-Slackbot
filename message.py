import json


class Message:
    def __init__(self, message_file):
        try:
            new_message = json.load(open(message_file))
            self.device = new_message["device"]
            self.text = new_message["message"]
            self.timestamp = new_message["timestamp"]
        except BaseException as err:
            output = [
                f"Error: could not load {message_file}",
                f"Error: {err}",
                ""
            ]
            print('\n'.join(output))
            history = open(message_file, "a")  # open the history file and log the rule
            history.write('\n'.join(output))
            history.close()

    def __str__(self):
        output = [
            f"Device: {self.device}",
            f"Message: {self.text}",
            f"Timestamp: {self.timestamp}",
            ""
        ]
        return '\n'.join(output)
