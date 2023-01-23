import os
import re
import json
import time
import subprocess
import shlex

configFile=os.path.expanduser("~/hermes.json")
config=json.load(open(configFile))


class Hermes:
    def __init__(self, config_file="~\\hermes.json"):
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
        except BaseException as err:
            output = [
                f"Error: could not load {self.configFile}",
                f"Error: {err}",
                ""
            ]
            print('\n'.join(output))

    def __str__(self):
        output = [
            "",
            f"Hermes: {self.systemName}",
            f"Configuration: {self.configFile}",
            "",
            f"Hermes started at {time.strftime('%Y%m%d-%H%M%S')} with the following values",
            f"Keyword: {self.keyword}",
            f"Message File: {self.messageFile}",
            f"History Directory: {self.historyDirectory}",
            f"App Directory: {self.appDirectory}",
            f"Rules Folder: {self.rulesDirectory}",
            ""
        ]
        return "\n".join(output)

    def check_for_message(self):
        return True if os.path.exists(self.messageFile) else False
