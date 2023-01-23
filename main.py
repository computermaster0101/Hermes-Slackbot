import os
import time

from hermes import Hermes
from message import Message
from messageProcessor import MessageProcessor

testing = True


def main():
    my_hermes = Hermes()
    print(my_hermes)

    if my_hermes.check_for_message():
        save_file = os.path.join(my_hermes.historyDirectory, f"{time.strftime('%Y%m%d-%H%M%S')}.{my_hermes.systemName}.txt")
        try:
            if testing:
                import shutil
                shutil.copy(my_hermes.messageFile, save_file)
            else:
                os.rename(my_hermes.messageFile, save_file)  # move the message to the log location
            new_message = Message(save_file)
            print(new_message)
            message_processor = MessageProcessor(save_file=save_file, message=new_message, rules_directory=my_hermes.rulesDirectory)
        except BaseException as error:
            print("something unexpected happened")
            print(error)


if __name__ == "__main__":
    main()
