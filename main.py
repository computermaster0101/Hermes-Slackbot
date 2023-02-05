import time
import threading
from message_processor import MessageProcessor
from message import Message
from audio_listener import AudioListener
from rule_set import RuleSet

import os
import json
import threading
import time


class Main:
    def __init__(self, config_file):
        self.configFile = os.path.expanduser(config_file)
        try:
            config = json.load(open(self.configFile))
            for item in config:
                config[item] = os.path.expanduser(config[item])
            self.systemName = config["sysName"]
            self.appDirectory = config["appDir"]
            self.rulesDirectory = config["rulesDir"]
            self.historyDirectory = config["histDir"]
            self.msgDir = config["msgDir"]
            self.messageFile = os.path.join(self.msgDir, f"{self.systemName}.txt")
            self.keyword = config["keyword"]

            self.audio_listener = AudioListener()
            self.rules = RuleSet(self.rulesDirectory)
            self.message_processor = MessageProcessor(self.rules)
            self.file_system_thread = threading.Thread(target=self.process_file_system_message)
            self.audio_thread = threading.Thread(target=self.process_audio_message)
        except FileNotFoundError as e:
            print(f"Error loading config from {self.configFile}: {e}")
        except Exception as e:
            print(f"Error loading config: {e}")

    def process_file_system_message(self):
        print(f"Listening for message file {self.messageFile}")
        while True:
            message = Message(message_file=self.messageFile)
            if message.timestamp:
                ## todo: reload rules incase rules have changed
                self.message_processor.process_message(message, self.rules)
            time.sleep(0.5)

    def process_audio_message(self):
        while True:
            audio_event = self.audio_listener.get_message_from_audio()
            message = Message(message_object=audio_event)
            ## todo: reload rules incase rules have changed
            if message.text:
                self.message_processor.process_message(message, self.rules)
            time.sleep(0.5)

    def run(self):
        print("commented out for testing")
        # self.file_system_thread.start()
        # self.audio_thread.start()


if __name__ == "__main__":
    main = Main("~\\hermes.json")
    main.run()
