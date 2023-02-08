from message_processor import MessageProcessor
from message import Message
from audio_listener import AudioListener
from rule_set import RuleSet

import os
import json
import threading
import time

env = "development"


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
            self.file_system_thread = threading.Thread(target=self.wait_for_file_system_message)
            self.audio_thread = threading.Thread(target=self.wait_for_audio_message)
        except FileNotFoundError as e:
            print(f"Error loading config from {self.configFile}: {e}")
        except Exception as e:
            print(f"Error loading config: {e}")

    def wait_for_file_system_message(self):
        print(f"Listening for message file {self.messageFile}")
        while True:
            if os.path.exists(self.messageFile):
                message = Message(message_file=self.messageFile)
                self.process_message(message)
            time.sleep(0.5)

    def wait_for_audio_message(self):
        print(f"Listening for keyword file {self.keyword}")
        while True:
            audio_event = self.audio_listener.get_message_from_audio()
            if audio_event:
                message = Message(message_object=audio_event)
                self.process_message(message)
            time.sleep(0.5)

    def process_message(self, message):
        self.rules = RuleSet(self.rulesDirectory)
        match, output = self.message_processor.process_message(message, self.rules)
        history_file = os.path.join(self.historyDirectory, f"{time.strftime('%Y%m%d-%H%M%S')}_{self.systemName}.txt")
        with open(history_file, "w") as f:
            f.write(f"{message}\n{output}")
        if env == "production":
            os.remove(self.messageFile)
        else:
            os.rename(self.messageFile, self.messageFile + ".bak")
        print(*map(print, output))

    def run(self):
        self.file_system_thread.start()
        self.audio_thread.start()
        self.file_system_thread.join()
        self.audio_thread.join()
        while True:
            time.sleep(1)


if __name__ == "__main__":
    main = Main("~\\hermes.json")
    main.run()
