import os
import re
import json
import time
import subprocess
import shlex

configFile = os.path.expanduser("~/hermes.json")
config = json.load(open(configFile))

for item in config:
    config[item] = os.path.expanduser(config[item])

systemName = config["sysName"]
appDirectory = config["appDir"]
rulesDirectory = config["rulesDir"]
historyDirectory = config["histDir"]
msgDir = config["msgDir"]
messageFile = os.path.join(msgDir, f"{systemName}.txt")

print(f"""
Hermes: {systemName}
Configuration: {configFile}

Hermes started at {time.strftime('%Y%m%d-%H%M%S')} with the following values
Message File: {messageFile}
History Directory: {historyDirectory}
App Directory: {appDirectory}
Rules Folder: {rulesDirectory}
""")

while not time.sleep(1):  # Continuously run
    if os.path.exists(messageFile):  # if a message file exists
        try:
            matched = False  # the new message has not yet been matched
            newMsg = json.load(open(messageFile))  # load the message file to a variable
            saveTo = os.path.join(historyDirectory, f"{time.strftime('%Y%m%d-%H%M%S')}.{systemName}.txt")  # identify the log location for the received message
            os.rename(messageFile, saveTo)  # move the message to the log location
            print(f"""
Device: {newMsg.get("device")}
Message: {newMsg.get("message")}
Timestamp: {newMsg.get("timestamp")}""")

            for file in os.listdir(rulesDirectory):  # for every file in the rules directory
                if file.endswith(".json"):  # only process json files
                    try:
                        rule = json.load(open(os.path.join(rulesDirectory, file)))  # load te rule file
                    except BaseException as err:
                        print(f"""
Failed Loading Rule: {file}
Error: {err}""")
                        history = open(saveTo, "a")  # open the history file and log the rule
                        history.write(f"""
Failed Loading Rule: {file}
Error: {err}""")
                        history.close()
                    for pattern in rule.get("patterns"):  # for every pattern
                        if re.search(pattern, newMsg.get("message")):  # check if the message matches the pattern
                            matched = True  # matched is true if the pattern/message matched
                            history = open(saveTo, "a")  # open the history file and log the rule
                            history.write(f"""
{rule}""")
                            history.close()
                            print(f"""
Rule: {rule.get("name")}
Pattern: {pattern}
Run Directory: {rule.get("runningDirectory")}
Pass Message: {rule.get("passMessage")}
Active: {rule.get("active")}""")

                            if rule["active"]:  # if the rule is active
                                ruleRunningDir = os.path.expanduser(rule.get("runningDirectory"))  # identify the running directory
                                if os.path.exists(ruleRunningDir): os.chdir(ruleRunningDir)  # if the running directory exists move to it
                                for action in rule["actions"]:  # for every action
                                    action = os.path.expanduser(action)  # make sure any ~ are expanded to the users directory
                                    if rule["passMessage"]:  # if the message should be sent with the action update the command
                                        cmd = (f"{action} \"{newMsg['message']}\"")
                                    else:
                                        cmd = action
                                    print(f"execution action: {cmd}")
                                    try:  # try to execute the user defined subprocess
                                        subprocess.Popen(shlex.split(cmd))
                                    except BaseException as err:  # if the os could not process the command, log there was an error
                                        print(f"""
Execution Failed: {cmd}: 
Error: {err}""")
                                        history = open(saveTo, "a")
                                        history.write(f"""
Command:"{cmd}" could not be exucuted by the OS 
Error: {err}""")
                                        history.close()
                                os.chdir(appDirectory)  # move back to the application directory

            if not matched:  # if the pattern/message does not match log it
                print(f"Undefined Pattern: {newMsg['message']}")
                history = open(saveTo, "a")
                history.write(f"""
Message:"{newMsg['message']}" does not match any defined patterns""")
                history.close()
        except BaseException as err:
            print(f"Unexpected Error: {err}")
            history = open(saveTo, "a")
            history.write(f"""
Unexpected Error: {err}""")
            history.close()
