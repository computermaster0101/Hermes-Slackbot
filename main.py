from message_processor import MessageProcessor
from message import Message
from audio_listener import AudioListener
from rule_set import RuleSet
from send_message import MessageSender

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

            if config["slack_token"]:
                self.slack_token = config["slack_token"]
                self.default_slack_channel = config["default_slack_channel"]
                self.message_sender = MessageSender(self.slack_token)

            self.audio_listener = AudioListener()
            self.rules = RuleSet(self.rulesDirectory)
            self.message_processor = MessageProcessor(self.rules)

            self.user_input_thread = threading.Thread(target=self.wait_for_user_message)
            self.file_system_thread = threading.Thread(target=self.wait_for_file_system_message)
            self.audio_thread = threading.Thread(target=self.wait_for_audio_message)
        except FileNotFoundError as e:
            print(f"Error loading config from {self.configFile}: {e}")
        except Exception as e:
            print(f"Error loading config: {e}")

    def wait_for_user_message(self):
        while True:
            user_input = input("Please enter a message: ")
            message = Message(message_text=user_input)
            self.process_message(message)

    def wait_for_file_system_message(self):
        print(f"Listen for message file {self.messageFile}")
        while True:
            if os.path.exists(self.messageFile):
                message = Message(message_file=self.messageFile)
                self.process_message(message)
            time.sleep(0.5)

    def wait_for_audio_message(self):
        print(f"Listen for keyword {self.keyword}")
        while True:
            audio_input = self.audio_listener.get_message_from_audio()
            if audio_input:
                message = Message(message_text=audio_input)
                self.process_message(message)
            time.sleep(0.5)

    def process_message(self, message):
        self.rules = RuleSet(self.rulesDirectory)
        match, output = self.message_processor.process_message(message, self.rules)
        history_file = os.path.join(self.historyDirectory, f"{time.strftime('%Y%m%d-%H%M%S')}_{self.systemName}.txt")
        with open(history_file, "w") as f:
            f.write(f"{message}\n")

            output_string = ""
            for line in output:
                output_string = f'{output_string}\n{line}'
            print(output_string)

            if hasattr(self, 'message_sender'):
                if message.channel:
                    self.message_sender.slack(output_string, message.channel)
                else:
                    self.message_sender.slack(output_string, self.default_slack_channel)

        if env == "production":
            os.remove(self.messageFile)
        else:
            if os.path.exists(self.messageFile + ".bak"):
                os.remove(self.messageFile + ".bak")
                os.rename(self.messageFile, self.messageFile + ".bak")

    def run(self):
        # self.audio_thread.start()
        # self.audio_thread.join()
        # self.file_system_thread.start()
        # self.file_system_thread.join()
        # self.user_input_thread.start()
        # self.user_input_thread.join()

        # self.wait_for_audio_message()
        # self.wait_for_file_system_message()
        self.wait_for_user_message()


if __name__ == "__main__":
    main = Main("~\\hermes.json")
    main.run()
