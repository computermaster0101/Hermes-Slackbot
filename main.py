import time
import threading

class Main:
    def __init__(self):
        self.message_processor = MessageProcessor()
        self.message = Message()
        self.audio_listener = AudioListener()
        self.rules = RuleSet()
        self.file_system_thread = threading.Thread(target=self.process_file_system_message)
        self.audio_thread = threading.Thread(target=self.process_audio_message)

    def process_file_system_message(self):
        while True:
            message = self.message.get_message_from_file_system()
            if message:
                self.message_processor.process_message(message, self.rules)
            time.sleep(0.5)

    def process_audio_message(self):
        while True:
            message = self.audio_listener.get_message_from_audio()
            if message:
                self.message_processor.process_message(message, self.rules)
            time.sleep(0.5)

    def run(self):
        self.file_system_thread.start()
        self.audio_thread.start()

if __name__ == "__main__":
    main = Main()
    main.run()
