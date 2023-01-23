class MessageProcessor:
    def __init__(self, save_file, message, rules_directory=''):
        self.matched = False
        self.saveFile = save_file  # identify the log location for the received message
        self.message = message
        self.rulesDirectory = rules_directory
        self.ruleDictionary = []


