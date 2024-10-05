# Todo:
# * test keyword
# * test file ingestion
# * test user input

from message_processor import MessageProcessor
from message import Message
from audio_listener import AudioListener
from rule_set import RuleSet
from send_message import MessageSender

import os
import threading
import time
from dotenv import load_dotenv

env = "dev"


class Main:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        try:
            # Initialize class variables from environment variables
            self.systemName = os.getenv("SYSNAME")
            self.appDirectory = os.getenv("APPDIR")
            self.rulesDirectory = os.getenv("RULESDIR")
            self.historyDirectory = os.getenv("HISTDIR")
            self.msgDir = os.getenv("MSGDIR")
            self.messageFile = os.path.join(self.msgDir, f"{self.systemName}.txt")
            self.keyword = os.getenv("KEYWORD")

            self.slack_token = os.getenv("SLACK_TOKEN")
            self.default_slack_channel = os.getenv("DEFAULT_SLACK_CHANNEL")

            if self.slack_token:
                self.message_sender = MessageSender(self.slack_token)

            self.audio_listener = AudioListener(keyword=self.keyword)
            self.rules = RuleSet(self.rulesDirectory)
            self.message_processor = MessageProcessor(self.rules)

            self.user_input_thread = threading.Thread(target=self.wait_for_user_message)
            self.file_system_thread = threading.Thread(target=self.wait_for_file_system_message)
            self.audio_thread = threading.Thread(target=self.wait_for_audio_message)

        except Exception as e:
            print(f"Error loading configuration: {e}")

    def wait_for_user_message(self):
        while True:
            try:
                user_input = input("Please enter a message: ")
                message = Message(message_text=user_input, message_file=None, device=self.systemName)
                print(message)
                self.process_message(message)
            except EOFError:
                print("\nExiting...\n")
                os._exit(0)
            except KeyboardInterrupt:
                print("\nExiting...\n")
                os._exit(0)

    def wait_for_file_system_message(self):
        print(f"Listening for message file {self.messageFile}")
        while True:
            if os.path.exists(self.messageFile):
                message = Message(message_file=self.messageFile, message_text=None)
                self.process_message(message, file=True)
            time.sleep(0.5)

    def wait_for_audio_message(self):
        print(f"Listening for keyword {self.keyword}")
        while True:
            audio_input = self.audio_listener.get_message_from_audio()
            if audio_input:
                message = Message(message_text=audio_input, message_file=None, device=self.systemName)
                self.process_message(message)
            time.sleep(0.5)

    def process_message(self, message, file=False):
        self.rules = RuleSet(self.rulesDirectory)
        if message.device == self.systemName:
            output = self.message_processor.process_message(message, self.rules)
        else:
            output = ["Invalid Message!"]

        history_file = os.path.join(self.historyDirectory, f"{time.strftime('%Y%m%d-%H%M%S')}_{self.systemName}.txt")

        output_string = "\n".join(output)

        print(output_string)
        with open(history_file, "w") as f:
            f.write(f"{message}\n{output_string}")

        if hasattr(self, 'message_sender'):
            if message.channel:
                self.message_sender.slack(output_string, message.channel)
            else:
                self.message_sender.slack(output_string, self.default_slack_channel)

        if env == "production":
            if file:
                os.remove(self.messageFile)
        else:
            if os.path.exists(self.messageFile + ".bak"):
                os.remove(self.messageFile + ".bak")
                os.rename(self.messageFile, self.messageFile + ".bak")

    def run(self):
        try:
            # self.audio_thread.start()
            self.file_system_thread.start()

            if hasattr(self, 'message_sender'):
                self.message_sender.slack(f'{self.systemName} started listening for messages', self.default_slack_channel)
            print(f'{self.systemName} started listening for messages')

            self.user_input_thread.start()
            self.user_input_thread.join()

            self.wait_for_user_message()

        except Exception as e:
            print(f'An unexpected error occurred: {e}')


if __name__ == "__main__":
    main = Main()
    main.run()
